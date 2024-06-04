import asyncio
import logging

from fastapi import Depends
from starlette.websockets import WebSocket, WebSocketDisconnect

from src.core.utils.collections import for_each, safe_json
from src.core.utils.websockets import ws_return_if_closed, is_websocket_connected
from src.main.components.auth.models.user import UserInternal
from src.main.components.auth.utils.dependencies.ws_auth import WSJWTBearerAuthDependency
from src.main.components.storage.exceptions import InvalidStorageRequestHTTPException
from src.main.components.storage.models.storage_data_message import StorageDataMessage, DataMessageType
from src.main.components.storage.repository import StorageRepositoryST
from src.main.exceptions import ApplicationHTTPException, SchemaValidationHTTPException
from src.main.http import SuccessResponse, ApplicationJsonResponse
from .schemas import StorageRequest, StorageRequestType
from .utils import send_storage_data_message_ws, send_application_response_ws
from ..router import storage_router

_logger = logging.getLogger(__name__)
_jwt_auth = WSJWTBearerAuthDependency()  # FIXME: Always respond 403 when there is error with connection
_storage_repository = StorageRepositoryST()


async def _parse_storage_request(data: str) -> StorageRequest:
    if (message := safe_json(data)) is None:
        raise InvalidStorageRequestHTTPException()

    try:
        return StorageRequest(**message)
    except ValueError as error:
        raise SchemaValidationHTTPException(validation_error=error)


async def _handle_recv_data(data: str, user: UserInternal) -> ApplicationJsonResponse:
    request = await _parse_storage_request(data)

    await _storage_repository.send_data_message(  # TODO: Response MUST BE valid ApplicationResponsePayload
        StorageDataMessage(
            data_type=DataMessageType.REQUEST if request.request_type == StorageRequestType.ENQUEUE_REQUEST else DataMessageType.RESPONSE,
            message_id=request.message_id,
            target_user_id=request.target_user_id,
            sender_user_id=user.id,
            data=request.data
        )
    )

    return SuccessResponse()


async def _listen_task(websocket: WebSocket, user: UserInternal) -> None:
    generator = _storage_repository.wait_for_data_message(user_id=user.id)

    try:
        # Sending data until access token is not expired; Then closing the connection
        async for schema in generator:
            if schema is None:  # TODO: Use timeout to handle access_token expiration
                continue

            await send_storage_data_message_ws(
                websocket=websocket,
                data=schema.to_json_dict(exclude="target_user_id")
            )
    except WebSocketDisconnect:
        _logger.debug(f"Storage listener {user.id}: websocket disconnected")
    except asyncio.CancelledError:
        _logger.debug(f"Storage listener {user.id}: task canceled")


@storage_router.websocket("/")
@ws_return_if_closed
async def storage_ws_route(websocket: WebSocket, user: UserInternal = Depends(_jwt_auth)) -> None:
    await websocket.accept()

    listen_task = asyncio.create_task(_listen_task(websocket, user))

    while is_websocket_connected(websocket):
        recv_task = asyncio.create_task(websocket.receive())

        done, pending = await asyncio.wait([listen_task, recv_task], return_when=asyncio.FIRST_COMPLETED)

        try:
            if recv_task.done():
                received = recv_task.result()

                if received is not None and (received_data := received.get("text")) is not None:
                    response = await _handle_recv_data(received_data,
                        user)  # Hack (because I've already written generics for it)
                    await send_application_response_ws(websocket, payload=response.payload)
            if listen_task.done():
                await listen_task  # Just to raise an error, if there is one
        except ApplicationHTTPException as error:  # Hack (because I've already written generics for it)
            await send_application_response_ws(websocket, payload=error.payload)
        except WebSocketDisconnect:
            return
        except Exception as error:
            _logger.warning(f"Got unknown error in storage ws: {error.__class__.__name__}: {error}")
            for_each(asyncio.Task.cancel, pending)
            raise error

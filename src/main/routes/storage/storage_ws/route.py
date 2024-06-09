import asyncio
import logging

from fastapi import Depends
from starlette.websockets import WebSocket, WebSocketDisconnect

from src.core.utils.collections import for_each
from src.core.utils.websockets import ws_return_if_closed, is_websocket_connected
from src.main.components.auth.models.user import UserInternal
from src.main.components.auth.utils.dependencies.ws_auth import WSJWTBearerAuthDependency
from src.main.components.storage.repository import StorageRepositoryST
from .utils import send_storage_data_message_ws
from ..router import storage_router

_logger = logging.getLogger(__name__)
_jwt_auth = WSJWTBearerAuthDependency()  # FIXME: Always respond 403 when there is error with connection
_storage_repository = StorageRepositoryST()


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
        _logger.debug(f"Storage listener (user {user.id}): websocket disconnected")
    except asyncio.CancelledError:
        _logger.debug(f"Storage listener (user {user.id}): task canceled")


@storage_router.websocket("/")
@ws_return_if_closed
async def storage_ws_route(websocket: WebSocket, user: UserInternal = Depends(_jwt_auth)) -> None:
    await websocket.accept()

    listen_task = asyncio.create_task(_listen_task(websocket, user))
    while is_websocket_connected(websocket):
        receive_task = asyncio.create_task(websocket.receive_text())
        done, pending = await asyncio.wait([listen_task, receive_task], return_when=asyncio.FIRST_COMPLETED)

        try:
            await asyncio.gather(*done)
        except WebSocketDisconnect:
            _logger.debug(f"Storage ws (user {user.id}) disconnected")
        except Exception as error:
            for_each(asyncio.Task.cancel, pending)
            raise error

    if not listen_task.done():
        listen_task.cancel()

import uuid

from fastapi import Depends

from src.main.components.auth.models.user import UserInternal
from src.main.components.auth.utils.dependencies.http_auth import HTTPJWTBearerAuthDependency
from src.main.components.storage.models.storage_data_message import StorageDataMessage, DataMessageType
from src.main.components.storage.repository import StorageRepositoryST
from src.main.http import ApplicationJsonResponse
from src.main.http.responses import SuccessResponse
from .schemas import WriteRequestPayload, WriteResponsePayload, StorageWriteResponsePayload
from ..router import storage_router

_jwt_auth = HTTPJWTBearerAuthDependency()
_storage_repository = StorageRepositoryST()


@storage_router.post("/write/request/")
async def storage_write_request_route(payload: WriteRequestPayload, user: UserInternal = Depends(_jwt_auth)) -> ApplicationJsonResponse:
    request_uuid = str(uuid.uuid4())
    await _storage_repository.send_data_message(
        StorageDataMessage(
            data_type=DataMessageType.REQUEST,
            request_uuid=request_uuid,
            target_user_id=payload.target_user_id,
            sender_user_id=user.id,
            data=payload.data
        )
    )

    return SuccessResponse(data=StorageWriteResponsePayload(request_uuid=request_uuid))


@storage_router.post("/write/response/")
async def storage_write_response_route(payload: WriteResponsePayload, user: UserInternal = Depends(_jwt_auth)) -> ApplicationJsonResponse:
    await _storage_repository.send_data_message(
        StorageDataMessage(
            data_type=DataMessageType.RESPONSE,
            request_uuid=payload.response_to_request_uuid,
            target_user_id=payload.target_user_id,
            sender_user_id=user.id,
            data=payload.data
        )
    )

    return SuccessResponse()

from fastapi import Depends

from src.main.components.auth.models.user import UserInternal, UserPublic
from src.main.components.auth.utils.dependencies.http_auth import HTTPJWTBearerAuthDependency
from src.main.components.devices.repository.devices_repository import DevicesRepositoryST
from src.main.exceptions.http.generics import ForbiddenHTTPException
from src.main.http import ApplicationJsonResponse
from src.main.http.responses import SuccessResponse
from .schemas import OwnerResponsePayload
from ..router import devices_router

_jwt_auth = HTTPJWTBearerAuthDependency()
_devices_repository = DevicesRepositoryST()


@devices_router.get("/me/owner/")
async def get_owner_route(user: UserInternal = Depends(_jwt_auth)) -> ApplicationJsonResponse:
    if not user.is_device:
        raise ForbiddenHTTPException(message="Non-device user can not have owner")

    owner = await _devices_repository.get_device_owner(user.id)

    return SuccessResponse(
        data=OwnerResponsePayload(
            owner=owner.convert_to(UserPublic) if owner is not None else None
        )
    )

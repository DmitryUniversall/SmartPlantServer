from fastapi import Depends

from src.main.components.auth.models.user import UserInternal, UserPublic
from src.main.components.auth.utils.dependencies.http_auth import HTTPJWTBearerAuthDependency
from src.main.components.devices.repository.devices_repository import DevicesRepositoryST
from src.main.exceptions.http.generics import ForbiddenHTTPException
from src.main.http import ApplicationJsonResponse
from src.main.http.responses import SuccessResponse
from .schemas import DevicesResponsePayload
from ..router import devices_router

_jwt_auth = HTTPJWTBearerAuthDependency()
_devices_repository = DevicesRepositoryST()


@devices_router.get("/")
async def get_devices_route(user: UserInternal = Depends(_jwt_auth)) -> ApplicationJsonResponse:
    if user.is_device:
        raise ForbiddenHTTPException(message="Only non-device user can have devices")

    devices_internal = await _devices_repository.get_devices(user)
    devices = list(map(lambda x: x.convert_to(UserPublic), devices_internal))

    return SuccessResponse(
        data=DevicesResponsePayload(
            devices=devices
        )
    )

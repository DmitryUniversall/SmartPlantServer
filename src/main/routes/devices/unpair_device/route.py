from fastapi import Depends

from src.main.components.auth.models.user import UserInternal
from src.main.components.auth.utils.dependencies.http_auth import HTTPJWTBearerAuthDependency
from src.main.components.devices.repository.devices_repository import DevicesRepositoryST
from src.main.exceptions import fetch_or_404
from src.main.http import ApplicationJsonResponse
from src.main.http.responses import SuccessResponse
from ..router import devices_router

_jwt_auth = HTTPJWTBearerAuthDependency()
_devices_repository = DevicesRepositoryST()


@devices_router.post("/device/{device_id}/unpair/")
async def unpair_device_route(device_id: int, user: UserInternal = Depends(_jwt_auth)) -> ApplicationJsonResponse:
    with fetch_or_404():
        device_pair = await _devices_repository.get_pair_by_ids(user.id, device_id)

    await _devices_repository.unpair(device_pair)
    return SuccessResponse()

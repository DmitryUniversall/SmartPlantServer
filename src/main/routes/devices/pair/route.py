import asyncio
from http import HTTPStatus
from typing import Union

from fastapi import Depends

from src.core.state import project_settings
from src.core.utils.errors import supress_exception
from src.main.components.auth.models.user import UserInternal, UserPublic
from src.main.components.auth.repository import AuthRepositoryST
from src.main.components.auth.utils.dependencies.http_auth import HTTPJWTBearerAuthDependency
from src.main.components.devices.exceptions import InvalidUserOrDeviceHTTPException
from src.main.components.devices.models.device_pair_request import DevicePairRequest, DevicePairReqeustState
from src.main.components.devices.repository.devices_repository import DevicesRepositoryST
from src.main.exceptions import fetch_or_404
from src.main.exceptions.http.generics import ForbiddenHTTPException
from src.main.http import ApplicationJsonResponse
from src.main.http.responses import SuccessResponse
from .schemas import PairDeviceResponsePayload
from ..router import devices_router

_jwt_auth = HTTPJWTBearerAuthDependency()
_auth_repository = AuthRepositoryST()
_devices_repository = DevicesRepositoryST()


@devices_router.post("/device/{device_identifier}/pair/")
async def pair_device_route(
        device_identifier: Union[int, str],
        user: UserInternal = Depends(_jwt_auth)
) -> ApplicationJsonResponse:
    if user.is_device:
        raise ForbiddenHTTPException(message="Only non-device user can send pair requests")

    with fetch_or_404():
        if isinstance(device_identifier, int):
            device_user = await _auth_repository.get_user_by_id(device_identifier)  # type: ignore
        else:
            device_user = await _auth_repository.get_user_by_username(device_identifier)  # type: ignore

    if not device_user.is_device:
        raise InvalidUserOrDeviceHTTPException(status_code=HTTPStatus.BAD_REQUEST, message="Specified device user is not device")

    request = DevicePairRequest(
        user=user,
        device=device_user
    )

    await _devices_repository.send_pair_reqeust(request)
    with supress_exception(asyncio.TimeoutError):
        await request.wait_for_state_change(timeout=30)

    return SuccessResponse(
        **(
            project_settings.APPLICATION_STATUS_CODES.DEVICES.PAIR_REQUEST_ACCEPTED
            if request.state == DevicePairReqeustState.ACCEPTED else
            project_settings.APPLICATION_STATUS_CODES.DEVICES.PAIR_REQUEST_REJECTED
        ),
        data=(
            PairDeviceResponsePayload(device_user=device_user.convert_to(UserPublic))
            if request.state == DevicePairReqeustState.ACCEPTED else
            None
        )
    )

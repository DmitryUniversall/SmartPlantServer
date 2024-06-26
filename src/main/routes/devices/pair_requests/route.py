from fastapi import Depends

from src.main.components.auth.models.user import UserInternal
from src.main.components.auth.utils.dependencies.http_auth import HTTPJWTBearerAuthDependency
from src.main.components.devices.repository.devices_repository import DevicesRepositoryST
from src.main.exceptions import BadRequestHTTPException
from src.main.http import ApplicationJsonResponse
from src.main.http.responses import UpdatedResponse, SuccessResponse
from .schemas import PairRequestsResponsePayload, PairRequestRespondAction
from ..router import devices_router
from src.main.exceptions.http import ForbiddenHTTPException

_jwt_auth = HTTPJWTBearerAuthDependency()
_devices_repository = DevicesRepositoryST()


@devices_router.get("/me/pair/requests/")
async def pair_requests_get_route(user: UserInternal = Depends(_jwt_auth)) -> ApplicationJsonResponse:
    if not user.is_device:
        raise BadRequestHTTPException(message="User is not device, so it cannot receive pair requests")

    pair_requests = await _devices_repository.get_pair_requests(device_id=user.id)

    return SuccessResponse(
        data=PairRequestsResponsePayload(
            pair_requests=pair_requests
        )
    )


@devices_router.post("/me/pair/requests/request/{request_uuid}/{action}/")
async def pair_requests_post_route(request_uuid: str, action: str, user: UserInternal = Depends(_jwt_auth)) -> ApplicationJsonResponse:
    try:
        action_enum = PairRequestRespondAction[action.upper()]
    except KeyError as error:
        raise BadRequestHTTPException(message="Unknown action") from error

    pair_request = await _devices_repository.get_pair_request(request_uuid)

    if pair_request.device.id != user.id:
        raise ForbiddenHTTPException()

    if action_enum == PairRequestRespondAction.ACCEPT:
        await _devices_repository.accept_pair_request(pair_request)
    else:
        await _devices_repository.reject_pair_request(pair_request)

    return UpdatedResponse()

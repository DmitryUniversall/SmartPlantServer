from http import HTTPStatus

from src.core.state import project_settings
from src.main.components.auth.repository import AuthRepositoryST
from src.main.http import ApplicationJsonResponse
from src.main.models import ApplicationResponsePayload
from .schemas import RefreshRequestPayload, RefreshResponsePayload
from ..router import auth_router

_auth_repository = AuthRepositoryST()


@auth_router.post("/refresh/")
async def refresh_route(token: RefreshRequestPayload) -> ApplicationJsonResponse:
    _, token_pair = await _auth_repository.refresh(token.refresh_token)

    return ApplicationJsonResponse(
        status_code=HTTPStatus.OK,
        content=ApplicationResponsePayload[RefreshResponsePayload](
            **project_settings.APPLICATION_STATUS_CODES.GENERICS.SUCCESS,
            data=RefreshResponsePayload(
                tokens=token_pair
            )
        )
    )

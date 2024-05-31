from src.core.state import project_settings
from src.main.components.auth.repository import AuthRepositoryST
from src.main.http import ApplicationJsonResponse
from src.main.models import ApplicationResponsePayload
from .schemas import RefreshPayload, RefreshResponse
from ..router import auth_router

_auth_repository = AuthRepositoryST()


@auth_router.post("/refresh/")
async def refresh_route(token: RefreshPayload) -> ApplicationJsonResponse:
    _, token_pair = await _auth_repository.refresh(token.refresh_token)

    return ApplicationJsonResponse(
        status_code=200,
        content=ApplicationResponsePayload[RefreshResponse](
            **project_settings.APPLICATION_STATUS_CODES.GENERICS.SUCCESS,
            data=RefreshResponse(
                tokens=token_pair
            )
        )
    )

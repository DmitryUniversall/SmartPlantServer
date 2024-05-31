from src.core.state import project_settings
from src.main.components.auth.models.user import UserPrivate
from src.main.components.auth.repository import AuthRepositoryST
from src.main.http import ApplicationJsonResponse
from src.main.models import ApplicationResponsePayload

from .schemas import LoginPayload, LoginResponse
from ..router import auth_router

_auth_repository = AuthRepositoryST()


@auth_router.post("/login/")
async def login_route(payload: LoginPayload) -> ApplicationJsonResponse:
    user_internal, token_pair = await _auth_repository.login(**payload.model_dump())

    return ApplicationJsonResponse(
        status_code=200,
        content=ApplicationResponsePayload[LoginResponse](
            **project_settings.APPLICATION_STATUS_CODES.GENERICS.SUCCESS,
            data=LoginResponse(
                user=user_internal.convert_to(UserPrivate),
                tokens=token_pair
            )
        )
    )

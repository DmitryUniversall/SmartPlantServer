from http import HTTPStatus

from src.core.state import project_settings
from src.main.components.auth.models.user import UserPrivate
from src.main.components.auth.repository import AuthRepositoryST
from src.main.http import ApplicationJsonResponse
from src.main.models import ApplicationResponsePayload
from .schemas import RegisterReqeustPayload, RegisterResponsePayload
from ..router import auth_router

_auth_repository = AuthRepositoryST()


@auth_router.post("/register/")
async def register_route(payload: RegisterReqeustPayload) -> ApplicationJsonResponse:
    user_internal, token_pair = await _auth_repository.register(**payload.model_dump())

    return ApplicationJsonResponse(
        status_code=HTTPStatus.CREATED,
        content=ApplicationResponsePayload[RegisterResponsePayload](
            **project_settings.APPLICATION_STATUS_CODES.GENERICS.CREATED,
            data=RegisterResponsePayload(
                user=user_internal.convert_to(UserPrivate),
                tokens=token_pair
            )
        )
    )

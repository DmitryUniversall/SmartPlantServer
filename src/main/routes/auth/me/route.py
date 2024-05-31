from fastapi import Depends

from src.core.state import project_settings
from src.main.components.auth.models.user import UserInternal, UserPrivate
from src.main.components.auth.utils.dependencies.http_auth import HTTPJWTBearerAuthDependency
from src.main.http import ApplicationJsonResponse
from src.main.models import ApplicationResponsePayload
from .schemas import GetMeResponse
from ..router import auth_router

_jwt_auth = HTTPJWTBearerAuthDependency()


@auth_router.get("/me/")
async def get_me_route(user: UserInternal = Depends(_jwt_auth)) -> ApplicationJsonResponse:
    return ApplicationJsonResponse(
        status_code=200,
        content=ApplicationResponsePayload[GetMeResponse](
            **project_settings.APPLICATION_STATUS_CODES.GENERICS.SUCCESS,
            data=GetMeResponse(
                user=user.convert_to(UserPrivate)
            )
        )
    )

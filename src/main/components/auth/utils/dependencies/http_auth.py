from starlette.requests import Request

from src.main.components.auth.models.user import UserInternal
from src.main.components.auth.repository import AuthRepositoryST
from src.main.components.auth.utils.bearer_auth_mixin import BearerAuthMixin

_auth_repository = AuthRepositoryST()


class HTTPJWTBearerAuthDependency(BearerAuthMixin):
    async def __call__(self, request: Request) -> UserInternal:
        authorization = request.headers.get("Authorization")

        access_token = await self.extract_token(authorization)
        return await _auth_repository.authenticate(access_token)

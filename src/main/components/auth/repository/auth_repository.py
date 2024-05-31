from typing import Tuple

from src.core.utils.singleton import SingletonMeta
from src.main.components.auth.internal_utils.authenticator import JWTAuthenticatorST
from src.main.components.auth.models.auth_token_pair import AuthTokenPair
from src.main.components.auth.models.user import UserInternal

_authenticator = JWTAuthenticatorST()


class AuthRepositoryST(metaclass=SingletonMeta):
    async def authenticate(self, access_token: str) -> UserInternal:
        return await _authenticator.authenticate(access_token)

    async def refresh(self, refresh_token: str) -> Tuple[UserInternal, AuthTokenPair]:
        return await _authenticator.refresh(refresh_token)

    async def register(self, username: str, password: str, **fields) -> Tuple[UserInternal, AuthTokenPair]:
        return await _authenticator.register(username, password, **fields)

    async def login(self, username: str, password: str, **fields) -> Tuple[UserInternal, AuthTokenPair]:
        return await _authenticator.login(username, password, **fields)

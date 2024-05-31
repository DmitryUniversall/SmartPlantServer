from src.core.db import BaseSchema
from src.main.components.auth.models.auth_token_pair import AuthTokenPair
from src.main.components.auth.models.user import UserPrivate


class LoginPayload(BaseSchema):
    username: str
    password: str


class LoginResponse(BaseSchema):
    user: UserPrivate
    tokens: AuthTokenPair

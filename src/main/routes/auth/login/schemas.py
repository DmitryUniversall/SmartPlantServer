from src.core.db import BaseSchema
from src.main.components.auth.models.auth_token_pair import AuthTokenPair
from src.main.components.auth.models.user import UserPrivate


class LoginRequestPayload(BaseSchema):
    username: str
    password: str


class LoginResponsePayload(BaseSchema):
    user: UserPrivate
    tokens: AuthTokenPair

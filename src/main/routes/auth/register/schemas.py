from src.core.db import BaseSchema
from src.main.components.auth.models.auth_token_pair import AuthTokenPair
from src.main.components.auth.models.user import UserPrivate


class RegisterReqeustPayload(BaseSchema):
    username: str
    password: str
    is_device: bool = False


class RegisterResponsePayload(BaseSchema):
    user: UserPrivate
    tokens: AuthTokenPair

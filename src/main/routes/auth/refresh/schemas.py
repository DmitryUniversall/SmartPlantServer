from src.core.db import BaseSchema
from src.main.components.auth.models.auth_token_pair import AuthTokenPair


class RefreshPayload(BaseSchema):
    refresh_token: str


class RefreshResponse(BaseSchema):
    tokens: AuthTokenPair

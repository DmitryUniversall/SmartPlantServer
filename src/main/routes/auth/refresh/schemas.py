from src.core.db import BaseSchema
from src.main.components.auth.models.auth_token_pair import AuthTokenPair


class RefreshRequestPayload(BaseSchema):
    refresh_token: str


class RefreshResponsePayload(BaseSchema):
    tokens: AuthTokenPair

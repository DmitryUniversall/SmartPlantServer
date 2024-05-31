from datetime import datetime, timedelta
from typing import Literal

from pydantic import Field

from src.core.state import project_settings
from .auth_token_payload import AuthTokenPayload, AuthTokenType


class AccessTokenPayload(AuthTokenPayload):
    token_type: Literal[AuthTokenType.ACCESS] = AuthTokenType.ACCESS
    exp: datetime = Field(
        default_factory=lambda: datetime.now() + timedelta(seconds=project_settings.ACCESS_TOKEN_EXPIRE)
    )

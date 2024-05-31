from datetime import datetime, timedelta
from typing import Literal

from pydantic import Field

from src.core.state import project_settings
from .auth_token_payload import AuthTokenPayload, AuthTokenType


class RefreshTokenPayload(AuthTokenPayload):
    token_type: Literal[AuthTokenType.REFRESH] = AuthTokenType.REFRESH
    exp: datetime = Field(
        default_factory=lambda: datetime.now() + timedelta(seconds=project_settings.REFRESH_TOKEN_EXPIRE)
    )

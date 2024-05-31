from typing import Optional

from src.core.state import project_settings
from src.main.components.auth.exceptions import (
    AuthorizationNotSpecifiedHTTPException,
    AuthorizationInvalidHTTPException,
    AuthorizationTypeUnknownHTTPException,
    TokenNotSpecifiedHTTPException
)


class BearerAuthMixin:
    async def extract_token(self, header: Optional[str]) -> str:
        _auth_status_codes = project_settings.APPLICATION_STATUS_CODES.AUTH

        if not header:
            raise AuthorizationNotSpecifiedHTTPException(status_code=403)
        elif len(header.split(" ")) != 2:
            raise AuthorizationInvalidHTTPException(status_code=403)

        type_, access_token = header.split(" ")
        if type_.lower() != "bearer":
            raise AuthorizationTypeUnknownHTTPException(status_code=403)
        elif not access_token:
            raise TokenNotSpecifiedHTTPException(status_code=403)

        return access_token

from typing import Optional, Dict

from src.core.exceptions.base import BaseApplicationError
from src.main.models.application_response import ApplicationResponsePayload


class ApplicationHTTPException(BaseApplicationError):
    def __init__(self, *, payload: ApplicationResponsePayload, headers: Optional[Dict[str, str]] = None) -> None:
        super().__init__(payload.message)

        self.payload: ApplicationResponsePayload = payload
        self.headers = headers

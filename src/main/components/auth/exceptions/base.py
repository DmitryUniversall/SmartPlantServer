from abc import abstractmethod
from typing import Optional

from src.main.exceptions import ApplicationHTTPException
from src.main.models import ApplicationResponsePayload


class AuthHTTPException(ApplicationHTTPException):
    def __init__(self, *, payload: Optional[ApplicationResponsePayload] = None, **kwargs) -> None:
        if payload is None:
            payload = self.get_default_response_payload()

        super().__init__(payload=payload, **kwargs)

    @abstractmethod
    def get_default_response_payload(self) -> ApplicationResponsePayload:
        ...

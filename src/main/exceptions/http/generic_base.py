from abc import abstractmethod, ABC
from typing import Optional, Dict

from src.main.models import ApplicationResponsePayload
from .base import ApplicationHTTPException


class GenericApplicationHTTPException(ApplicationHTTPException, ABC):
    def __init__(
            self,
            *,
            payload: Optional[ApplicationResponsePayload] = None,
            status_code: int,
            headers: Optional[Dict[str, str]] = None,
            **payload_kwargs
    ) -> None:
        if payload is None:
            payload = self.get_default_response_payload(**payload_kwargs)

        super().__init__(payload=payload, status_code=status_code, headers=headers)

    @abstractmethod
    def get_default_response_payload(self, **payload_kwargs) -> ApplicationResponsePayload:
        ...

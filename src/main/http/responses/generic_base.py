from abc import ABC, abstractmethod
from typing import Optional, Dict

from starlette.background import BackgroundTask

from src.core.state import project_settings
from src.main.models import ApplicationResponsePayload
from .json_response import ApplicationJsonResponse
from functools import reduce


class BaseGenericApplicationJsonResponse(ApplicationJsonResponse, ABC):
    def __init__(
            self,
            *,
            status_code: int,
            payload: Optional[ApplicationResponsePayload] = None,
            headers: Optional[Dict[str, str]] = None,
            background: Optional[BackgroundTask] = None,
            **payload_kwargs
    ) -> None:
        if payload is None:
            payload = self.get_default_response_payload(**payload_kwargs)

        super().__init__(content=payload, status_code=status_code, headers=headers, background=background)

    @abstractmethod
    def get_default_response_payload(self, **payload_kwargs) -> ApplicationResponsePayload:
        ...


class GenericApplicationJsonResponse(BaseGenericApplicationJsonResponse):
    default_ok: int
    default_status_code: int
    default_status_info_path: str

    def __init__(self, **kwargs) -> None:
        kwargs.setdefault("status_code", getattr(self.__class__, "default_status_code"))
        super().__init__(**kwargs)

    def get_default_response_payload(self, **payload_kwargs) -> ApplicationResponsePayload:
        path = getattr(self.__class__, "default_status_info_path").split(".")
        default_status_info = reduce(getattr, path, project_settings.APPLICATION_STATUS_CODES)

        return ApplicationResponsePayload(**{
            "ok": getattr(self.__class__, "default_ok"),
            **default_status_info,
            **payload_kwargs
        })

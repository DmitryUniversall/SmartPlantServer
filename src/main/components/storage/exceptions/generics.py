from http import HTTPStatus

from src.core.state import project_settings
from src.main.models import ApplicationResponsePayload
from .base import StorageHTTPException


class InvalidStorageRequestHTTPException(StorageHTTPException):
    def __init__(self, **kwargs) -> None:
        kwargs.setdefault("status_code", HTTPStatus.UNPROCESSABLE_ENTITY)
        super().__init__(**kwargs)

    def get_default_response_payload(self, **kwargs) -> ApplicationResponsePayload:
        return ApplicationResponsePayload(**{
            "ok": False,
            **project_settings.APPLICATION_STATUS_CODES.STORAGE.INVALID_STORAGE_REQUEST,
            **kwargs
        })

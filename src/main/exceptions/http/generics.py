from http import HTTPStatus

from src.core.state import project_settings
from src.main.models import ApplicationResponsePayload
from .generic_base import GenericApplicationHTTPException


class ForbiddenHTTPException(GenericApplicationHTTPException):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs, status_code=HTTPStatus.FORBIDDEN)

    def get_default_response_payload(self, **payload_kwargs) -> ApplicationResponsePayload:
        return ApplicationResponsePayload(**{
            "ok": False,
            **project_settings.APPLICATION_STATUS_CODES.GENERIC_ERRORS.FORBIDDEN,
            **payload_kwargs
        })


class NotFoundHTTPException(GenericApplicationHTTPException):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs, status_code=HTTPStatus.NOT_FOUND)

    def get_default_response_payload(self, **payload_kwargs) -> ApplicationResponsePayload:
        return ApplicationResponsePayload(**{
            "ok": False,
            **project_settings.APPLICATION_STATUS_CODES.GENERIC_ERRORS.NOT_FOUND,
            **payload_kwargs
        })


class BadRequestHTTPException(GenericApplicationHTTPException):
    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs, status_code=HTTPStatus.BAD_REQUEST)

    def get_default_response_payload(self, **payload_kwargs) -> ApplicationResponsePayload:
        return ApplicationResponsePayload(**{
            "ok": False,
            **project_settings.APPLICATION_STATUS_CODES.GENERIC_ERRORS.BAD_REQUEST,
            **payload_kwargs
        })

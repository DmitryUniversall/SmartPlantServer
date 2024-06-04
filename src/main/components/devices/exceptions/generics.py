from http import HTTPStatus

from src.core.state import project_settings
from src.main.models import ApplicationResponsePayload
from .base import DeviceHTTPException


class InvalidUserOrDeviceHTTPException(DeviceHTTPException):
    def __init__(self, **kwargs) -> None:
        kwargs.setdefault("status_code", HTTPStatus.BAD_REQUEST)
        super().__init__(**kwargs)

    def get_default_response_payload(self, **kwargs) -> ApplicationResponsePayload:
        return ApplicationResponsePayload(**{
            "ok": False,
            **project_settings.APPLICATION_STATUS_CODES.DEVICES.INVALID_USER_OR_DEVICE,
            **kwargs
        })


class DeviceAlreadyHasOwnerHTTPException(DeviceHTTPException):
    def __init__(self, **kwargs) -> None:
        kwargs.setdefault("status_code", HTTPStatus.BAD_REQUEST)
        super().__init__(**kwargs)

    def get_default_response_payload(self, **kwargs) -> ApplicationResponsePayload:
        return ApplicationResponsePayload(**{
            "ok": False,
            **project_settings.APPLICATION_STATUS_CODES.DEVICES.ALREADY_HAS_OWNER,
            **kwargs
        })


class CrossNetworkRequestHTTPException(DeviceHTTPException):
    def __init__(self, **kwargs) -> None:
        kwargs.setdefault("status_code", HTTPStatus.FORBIDDEN)
        super().__init__(**kwargs)

    def get_default_response_payload(self, **kwargs) -> ApplicationResponsePayload:
        return ApplicationResponsePayload(**{
            "ok": False,
            **project_settings.APPLICATION_STATUS_CODES.DEVICES.CROSS_NETWORK_REQUEST,
            **kwargs
        })

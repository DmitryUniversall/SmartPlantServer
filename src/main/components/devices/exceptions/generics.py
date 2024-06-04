from src.core.state import project_settings
from src.main.models import ApplicationResponsePayload
from .base import DeviceHTTPException


class InvalidUserOrDeviceHTTPException(DeviceHTTPException):
    def get_default_response_payload(self, **kwargs) -> ApplicationResponsePayload:
        return ApplicationResponsePayload(**{
            "ok": False,
            **project_settings.APPLICATION_STATUS_CODES.DEVICES.INVALID_USER_OR_DEVICE,
            **kwargs
        })


class DeviceAlreadyHasOwnerHTTPException(DeviceHTTPException):
    def get_default_response_payload(self, **kwargs) -> ApplicationResponsePayload:
        return ApplicationResponsePayload(**{
            "ok": False,
            **project_settings.APPLICATION_STATUS_CODES.DEVICES.ALREADY_HAS_OWNER,
            **kwargs
        })

from abc import ABC

from src.main.exceptions import GenericApplicationHTTPException


class DeviceHTTPException(GenericApplicationHTTPException, ABC):
    pass

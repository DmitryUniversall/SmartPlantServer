from abc import ABC

from src.main.exceptions import GenericApplicationHTTPException


class StorageHTTPException(GenericApplicationHTTPException, ABC):
    pass

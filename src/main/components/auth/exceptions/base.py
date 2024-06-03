from abc import ABC

from src.main.exceptions import GenericApplicationHTTPException


class AuthHTTPException(GenericApplicationHTTPException, ABC):
    pass

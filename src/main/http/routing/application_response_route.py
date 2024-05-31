from typing import Type

from src.core.http.routing import AbstractStaticResponseTypeApiRoute
from src.main.http.responses import ApplicationJsonResponse


class ApplicationResponseApiRoute(AbstractStaticResponseTypeApiRoute[ApplicationJsonResponse]):
    __response_type__: Type[ApplicationJsonResponse] = ApplicationJsonResponse

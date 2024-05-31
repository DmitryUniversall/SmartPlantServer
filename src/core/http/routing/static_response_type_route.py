from abc import ABC, abstractmethod
from typing import TypeVar, Generic, Coroutine, Any, Callable, Type

from fastapi.requests import Request
from fastapi.responses import Response
from fastapi.routing import APIRoute

_responseT = TypeVar('_responseT', bound=Response)


class AbstractStaticResponseTypeApiRoute(APIRoute, ABC, Generic[_responseT]):
    @property
    @abstractmethod
    def __response_type__(self) -> Type[_responseT]: ...

    def get_route_handler(self) -> Callable[[Request], Coroutine[Any, Any, Response]]:
        original_handler = super().get_route_handler()

        async def custom_handler(request: Request) -> Response:
            response = await original_handler(request)

            if not isinstance(response, self.__response_type__):
                raise TypeError(
                    f"[{self.__class__.__name__}]: Unexpected response type: must be {self.__response_type__.__name__}"
                )

            return response

        return custom_handler

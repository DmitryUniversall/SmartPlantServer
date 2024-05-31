from abc import ABC, abstractmethod
from functools import wraps
from typing import Type, Callable, Self

from fastapi.responses import Response


class AbstractErrorHandler(ABC):
    @property
    @abstractmethod
    def __exception_cls__(self) -> Type[Exception]:
        ...

    @abstractmethod
    async def handle(self, error: Exception) -> Response:
        ...

    @classmethod
    def as_error_handler(cls, exception_cls: Type[Exception], **init_kwargs) -> Callable:
        def decorator(coro) -> Type[Self]:
            @wraps(coro)
            async def wrapper(handler_self: 'AbstractErrorHandler', *args, **kwargs) -> Response:
                return await coro(*args, **kwargs, handler=handler_self)

            handler = type(coro.__name__, (cls,), {
                '__exception_cls__': exception_cls,
                'handle': wrapper
            })

            return handler(**init_kwargs)

        return decorator

    async def __call__(self, *args, **kwargs):
        return await self.handle(*args, **kwargs)

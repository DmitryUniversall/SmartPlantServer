from contextlib import contextmanager
from typing import Generator, Optional, Type
from src.core.db import BaseModel
from .generics import NotFoundHTTPException


@contextmanager
def fetch_or_404(exception_cls: Optional[Type[BaseModel.DoesNotExist]] = None) -> Generator[None, None, None]:
    try:
        yield
    except BaseModel.DoesNotExist as error:
        if exception_cls is not None and not isinstance(error, exception_cls):
            raise error

        raise NotFoundHTTPException(message="Requested object not found")

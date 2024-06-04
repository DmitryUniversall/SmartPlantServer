from contextlib import contextmanager
from typing import Generator, Optional, Type
from src.core.db import BaseModel
from .generics import NotFoundHTTPException


@contextmanager
def fetch_or_404(message: Optional[str] = None) -> Generator[None, None, None]:
    try:
        yield
    except BaseModel.DoesNotExist as error:
        raise NotFoundHTTPException(message=message if message is not None else "Requested object not found") from error

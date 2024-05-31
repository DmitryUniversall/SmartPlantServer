import logging
from abc import ABC
from typing import TypeVar, Optional, Union

from src.core.utils.import_tools import import_object
from src.core.utils.types import MISSING
from .abc import AbstractLazyObject

_logger = logging.getLogger()
_T = TypeVar("_T")


class LazyObject(AbstractLazyObject[_T], ABC):
    """
    A lazy evaluation class for retrieving and caching objects.
    Subclasses the AbstractLazyObject class.

    Methods:
    - `__init__(self, object_name: str) -> None`
        Initializes the LazyObject instance.

    - `object_name(self) -> str`
        Returns the name of the lazy object.

    - `get_object(self) -> _T`
        Retrieves and returns the actual value of the lazy object.

    - `get(self) -> _T`
        Retrieves and returns the actual value of the lazy object, caching it for further calls.

    - `get_safe(self) -> Optional[_T]`
        Retrieves and returns the actual value of the lazy object safely, logging ImportError if raised.
    """

    def __init__(self, object_name: str) -> None:
        """
        Initializes the LazyObject instance.

        :param object_name: `str`
            The name of the lazy object.
        """

        self._object_name: str = object_name
        self._object: Union[_T, MISSING] = MISSING

    @property
    def object_name(self) -> str:
        """
        Returns the name of the lazy object.

        :return: `str`
            The name of the lazy object.
        """

        return self._object_name

    def get_object(self) -> _T:
        """
        Retrieves and returns the actual value of the lazy object.

        :return: `_T`
            The actual value of the lazy object.
        """

        return import_object(self._object_name)

    def get(self) -> _T:
        """
        Retrieves and returns the actual value of the lazy object, caching it for further calls.

        :return: `_T`
            The actual value of the lazy object.
        """

        if self._object is MISSING:
            self._object = self.get_object()

        return self._object  # type: ignore

    def get_safe(self) -> Optional[_T]:
        """
        Retrieves and returns the actual value of the lazy object safely, logging ImportError if raised.

        :return: `Optional[_T]`
            The actual value of the lazy object if available, otherwise None.
        """

        try:
            return self.get()
        except ImportError as error:
            _logger.debug(
                f"Ignoring error in {self.__class__.__name__}: {error.__class__.__name__}: {error}"
            )

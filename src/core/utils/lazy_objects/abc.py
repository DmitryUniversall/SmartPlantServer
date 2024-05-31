from abc import ABC, abstractmethod
from typing import TypeVar, Optional, Any, Type, Generic

_T = TypeVar("_T")


class AbstractLazyObject(ABC, Generic[_T]):
    """
    An abstract base class for lazy evaluation of objects.

    Subclasses must implement the abstract methods:
    - `object_name(self) -> str`: Returns the name of the lazy object.
    - `get(self) -> _T`: Retrieves and returns the actual value of the lazy object.
    - `get_safe(self) -> Optional[_T]`: Retrieves and returns the actual value of the lazy object, or None if not available.

    Methods:
    - `object_name(self) -> str`: Abstract method to be implemented by subclasses to return the name of the lazy object.
    - `get(self) -> _T`: Abstract method to be implemented by subclasses to retrieve the actual value of the lazy object.
    - `get_safe(self) -> Optional[_T]`: Abstract method to be implemented by subclasses to retrieve the actual value of the lazy object safely.
    - `__get__(self, instance: Optional[Any], owner: Type[Any]) -> _T`: Default implementation for the descriptor protocol.
    """

    @property
    @abstractmethod
    def object_name(self) -> str:
        """
        Returns the name of the lazy object.

        :return: `str`
            The name of the lazy object.
        """

    @abstractmethod
    def get(self) -> _T:
        """
        Retrieves and returns the actual value of the lazy object.

        :return: `_T`
            The actual value of the lazy object.
        """

    @abstractmethod
    def get_safe(self) -> Optional[_T]:
        """
        Retrieves and returns the actual value of the lazy object safely.

        :return: `Optional[_T]`
            The actual value of the lazy object if available, otherwise None.
        """

    def __get__(self, instance: Optional[Any], owner: Type[Any]) -> _T:
        """
        Default implementation for the descriptor protocol.

        :param instance: `Optional[Any]`
            The instance that the attribute is accessed from.

        :param owner: `Type[Any]`
            The type of the instance.

        :return: `_T`
            The actual value of the lazy object.
        """

        return self.get()

from abc import abstractmethod
from typing import Any, Dict, Protocol, TypeVar, runtime_checkable, TypeAlias

_sizedIndexableReturnT = TypeVar("_sizedIndexableReturnT", covariant=True)


@runtime_checkable
class SizedIndexable(Protocol[_sizedIndexableReturnT]):
    @abstractmethod
    def __len__(self) -> int: ...

    @abstractmethod
    def __getitem__(self) -> _sizedIndexableReturnT: ...


class _MissingSentinel:
    """
    A special sentinel class representing a missing value.
    """

    __slots__ = ()

    def __bool__(self) -> bool:
        return False

    def __hash__(self) -> int:
        return 0

    def __repr__(self):
        return '...'

    def __str__(self) -> str:
        return "..."


MISSING: Any = _MissingSentinel()
JsonDict: TypeAlias = Dict[str, Any]

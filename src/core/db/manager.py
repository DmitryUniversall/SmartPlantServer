from abc import ABC, abstractmethod
from typing import AsyncContextManager, Self

from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession


class AbstractAsyncDatabaseManager(ABC):
    @property
    @abstractmethod
    def engine(self) -> AsyncEngine: ...

    @abstractmethod
    def session(self) -> AsyncContextManager[AsyncSession]: ...

    @abstractmethod
    async def initialize(self) -> Self: ...

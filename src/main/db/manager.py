from abc import ABCMeta
from logging import getLogger
from typing import Optional, Callable, AsyncContextManager, Generator, Any, Self

from sqlalchemy.ext.asyncio import AsyncSession, AsyncEngine, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.core.db import AbstractAsyncDatabaseManager
from src.core.exceptions import InitializationError
from src.core.state import project_settings
from src.core.utils.singleton import SingletonMeta
from .async_session_wrappers import (
    async_session_error_convert_wrapper,
    async_session_autorollback_wrapper
)

_logger = getLogger(__name__)


class _AsyncDatabaseManagerSTMeta(ABCMeta, SingletonMeta):
    pass


class AsyncDatabaseManagerST(AbstractAsyncDatabaseManager, metaclass=_AsyncDatabaseManagerSTMeta):
    def __init__(self) -> None:
        self._database_url: str = project_settings.DATABASE_URL
        self._engine: Optional[AsyncEngine] = None
        self._session_factory: Optional[Callable[[], AsyncSession]] = None

    def __await__(self) -> Generator[Any, None, Self]:
        return self.initialize().__await__()

    @property
    def engine(self) -> AsyncEngine:
        if self._engine is None:
            raise InitializationError(f"Unable to get async_engine: {self.__class__.__name__} is not initialized yet")

        return self._engine

    async def initialize(self) -> Self:
        self._engine = create_async_engine(self._database_url, pool_pre_ping=True)
        self._session_factory = sessionmaker(  # type: ignore
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

        return self

    def session(self) -> AsyncContextManager[AsyncSession]:
        if self._session_factory is None:
            raise InitializationError(f"Unable to get session: {self.__class__.__name__} is not initialized yet")

        return async_session_error_convert_wrapper(
            async_session_autorollback_wrapper(
                self._session_factory()
            )
        )

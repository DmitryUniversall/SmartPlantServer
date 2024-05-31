from contextlib import asynccontextmanager
from logging import getLogger
from typing import AsyncGenerator, AsyncContextManager

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.utils.errors import get_traceback_text
from .exceptions import error_mapping

_logger = getLogger(__name__)


@asynccontextmanager
async def async_session_autorollback_wrapper(
        context_manager: AsyncContextManager[AsyncSession]
) -> AsyncGenerator[AsyncSession, None]:
    async with context_manager as session:
        try:
            yield session
        except Exception as error:
            _logger.debug(f"Unknown error during db session; Rollback changes")
            await session.rollback()
            raise error
        finally:
            await session.close()


@asynccontextmanager
async def async_session_error_convert_wrapper(
        context_manager: AsyncContextManager[AsyncSession]
) -> AsyncGenerator[AsyncSession, None]:
    async with context_manager as session:
        try:
            yield session
        except IntegrityError as error:
            for key, value in error_mapping.items():
                if key not in str(error.orig).lower():
                    continue

                _logger.debug(f"Converting db error {error.orig.__class__.__name__} to {value.__name__} ({error.orig})")
                raise value(
                    message=str(error),
                    statement=error.statement,
                    params=error.params,
                    orig=error.orig,
                    hide_parameters=error.hide_parameters,
                    code=error.code,
                    ismulti=error.ismulti,
                )

            _logger.debug(f"Unknown error during db session:\n{get_traceback_text(error)}")
            raise error
        finally:
            await session.close()

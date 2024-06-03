import asyncio
import logging
from concurrent.futures import Executor
from functools import partial
from typing import Awaitable, TypeVar, Iterable, Coroutine, Union, Tuple, Callable, Any, Optional, Dict, List

_T = TypeVar("_T")
_K = TypeVar('_K')
_V = TypeVar('_V')

_logger = logging.getLogger(__name__)


async def gather_all(coros_or_futures: Iterable[Union[Coroutine, asyncio.Future]], **kwargs) -> Tuple[_T]:
    return tuple(await asyncio.gather(*coros_or_futures, **kwargs))


async def wait_with_timeout(coro: Awaitable[_T], *, timeout: Optional[float] = None, shield: bool = False) -> _T:
    return await asyncio.wait_for(
        asyncio.shield(coro) if shield else coro,
        timeout=timeout
    )


async def safe_wait_with_timeout(coro: Awaitable[_T], *, timeout: Optional[float] = None, shield: bool = False) -> Tuple[bool, Optional[_T]]:
    try:
        return True, await wait_with_timeout(coro, timeout=timeout, shield=shield)
    except asyncio.TimeoutError:
        return False, None


async def run_in_executor(executor: Optional[Executor], function: Callable, *args, **kwargs) -> Any:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, partial(function, *args, **kwargs))


async def _call_after(coro: Awaitable[_T], *, after: float) -> _T:
    await asyncio.sleep(after)
    return await coro


async def call_after(coro: Awaitable[_T], *, after: float) -> asyncio.Task[_T]:
    return asyncio.create_task(_call_after(coro, after=after))

import json
import logging
from typing import AsyncGenerator, Optional, TypeVar, Type, Generic

from redis import asyncio as aioredis

from src.core.db import BaseSchema
from src.core.utils.types import JsonDict
from src.main.redis.redis_client_manager import RedisClientManager

_logger = logging.getLogger(__name__)
_schemaT = TypeVar('_schemaT', bound=BaseSchema)


class RedisQueue(Generic[_schemaT]):
    def __init__(
            self,
            client_manager: RedisClientManager,
            schema_cls: Type[_schemaT],
            key: str,
            max_size: int = 5000,
            overflow_buffer: int = 100
    ) -> None:
        self._client_manager: RedisClientManager = client_manager
        self._schema_cls: Type[_schemaT] = schema_cls
        self._overflow_buffer = overflow_buffer
        self._max_size = max_size
        self._key = key

    async def _get_redis(self) -> aioredis.client.Redis:
        return await self._client_manager.get_redis()

    async def _write_data(self, data: str) -> None:
        redis = await self._get_redis()

        new_size = await redis.rpush(self._key, data)  # type: ignore
        if new_size > self._max_size:
            await redis.ltrim(self._key, self._max_size - self._overflow_buffer, -1)

    async def _write_json(self, data: JsonDict) -> None:
        await self._write_data(json.dumps(data))

    async def _read_data(self, *, timeout: int = 0) -> AsyncGenerator[Optional[str], None]:
        redis = await self._get_redis()

        while True:
            data = await redis.blpop([self._key], timeout=timeout)  # type: ignore
            yield None if data is None else data[1]

    async def _read_json(self, *, timeout: int = 0) -> AsyncGenerator[Optional[JsonDict], None]:
        async for data in self.read_data(key, timeout=timeout):  # type: ignore
            yield None if data is None else json.loads(data)

    async def write_schema(self, schema: _schemaT, **kwargs) -> None:
        if not isinstance(schema, self._schema_cls):
            raise TypeError(f"{self.__class__.__name__} can only contain objects of type {self._schema_cls.__name__}")

        await self._write_data(schema.model_dump_json(**kwargs))

    async def read_schema(self, *, timeout: int = 0, **kwargs) -> AsyncGenerator[Optional[_schemaT], None]:
        async for data in self._read_json(timeout=timeout):
            yield None if data is None else self._schema_cls.model_validate(data, **kwargs)

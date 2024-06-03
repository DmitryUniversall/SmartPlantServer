from typing import Optional

from src.core.state import project_settings
from src.core.utils.singleton import SingletonMeta
from src.main.redis import RedisClientManager


class AuthSessionManagerRedisST(RedisClientManager, metaclass=SingletonMeta):
    def __init__(self) -> None:
        super().__init__(db=project_settings.REDIS_DB_AUTH_SESSIONS)

    def get_active_access_key(self, user_id: int) -> str:
        return f"auth:tokens:user:{user_id}:access_token_uuid:active"

    def get_active_refresh_key(self, user_id: int) -> str:
        return f"auth:tokens:user:{user_id}:refresh_token_uuid:active"

    async def set_active_access_uuid(self, user_id: int, token_uuid: str) -> None:
        redis = await self.get_redis()
        await redis.setex(self.get_active_access_key(user_id), project_settings.ACCESS_TOKEN_REDIS_TTL, token_uuid)

    async def set_active_refresh_uuid(self, user_id: int, token_uuid: str) -> None:
        redis = await self.get_redis()
        await redis.setex(self.get_active_refresh_key(user_id), project_settings.REFRESH_TOKEN_REDIS_TTL, token_uuid)

    async def get_active_access_uuid(self, user_id: int) -> Optional[str]:
        redis = await self.get_redis()
        return await redis.get(self.get_active_access_key(user_id))

    async def get_active_refresh_uuid(self, user_id: int) -> Optional[str]:
        redis = await self.get_redis()
        return await redis.get(self.get_active_refresh_key(user_id))

    async def is_active_access(self, user_id: int, token_uuid: str) -> bool:
        return await self.get_active_access_uuid(user_id) == token_uuid

    async def is_active_refresh(self, user_id: int, token_uuid: str) -> bool:
        res = await self.get_active_refresh_uuid(user_id)
        return res == token_uuid

    async def get_access_ttl(self, user_id: int) -> int:
        redis = await self.get_redis()
        return await redis.ttl(self.get_active_access_key(user_id))  # type: ignore

    async def get_refresh_ttl(self, user_id: int) -> int:
        redis = await self.get_redis()
        return await redis.ttl(self.get_active_refresh_key(user_id))  # type: ignore

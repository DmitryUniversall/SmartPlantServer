from src.core.state import project_settings
from src.core.utils.singleton import SingletonMeta
from src.main.components.storage.internal_utils.storage_data_redis_queue import StorageDataRedisQueue
from src.main.redis import RedisClientManager


class StorageManagerRedisST(RedisClientManager, metaclass=SingletonMeta):
    def __init__(self) -> None:
        super().__init__(db=project_settings.REDIS_DB_DATA)

    def get_user_storage_queue_key(self, user_id: int) -> str:
        return f"storage:data:user:{user_id}:queue"

    def get_user_data_queue(self, user_id: int) -> StorageDataRedisQueue:
        return StorageDataRedisQueue(
            key=self.get_user_storage_queue_key(user_id),
            client_manager=self
        )

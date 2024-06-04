from src.main.redis.collections import RedisQueue
from src.main.components.storage.models.storage_data_message import StorageDataMessage


class StorageDataRedisQueue(RedisQueue[StorageDataMessage]):
    def __init__(self, **kwargs) -> None:
        super().__init__(schema_cls=StorageDataMessage, **kwargs)

from typing import AsyncGenerator, Optional

from src.core.utils.singleton import SingletonMeta
from src.main.components.auth.repository import AuthRepositoryST
from src.main.components.storage.internal_utils.storage_manager_redis import StorageManagerRedisST
from src.main.components.storage.models.storage_data_message import StorageDataMessage
from src.main.exceptions import fetch_or_404

_storage_manager = StorageManagerRedisST()
_auth_repository = AuthRepositoryST()


class StorageRepositoryST(metaclass=SingletonMeta):
    async def send_data_message(self, data_message: StorageDataMessage) -> None:
        with fetch_or_404(message="Unable to send data message: target user unknown"):
            await _auth_repository.get_user_by_id(data_message.target_device_id)

        queue = _storage_manager.get_user_data_queue(data_message.target_device_id)
        await queue.write_schema(data_message)

    def wait_for_data_message(self, user_id: int, **kwargs) -> AsyncGenerator[Optional[StorageDataMessage], None]:
        queue = _storage_manager.get_user_data_queue(user_id)
        return queue.read_schema(**kwargs)

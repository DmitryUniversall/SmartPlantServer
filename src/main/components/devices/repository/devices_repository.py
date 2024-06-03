from http import HTTPStatus
from typing import Optional, List

from src.core.utils.singleton import SingletonMeta
from src.main.components.auth.models.user import UserInternal
from src.main.components.devices.exceptions import DeviceAlreadyHasOwnerHTTPException
from src.main.components.devices.internal_utils.pair_request_manager import DevicePairRequestManagerST
from src.main.components.devices.models.device_pair_request import DevicePairRequest
from src.main.components.devices.resources.device_part_resource import DevicePairResourceST

_pair_manager = DevicePairRequestManagerST()
_device_pair_resource = DevicePairResourceST()


class DevicesRepositoryST(metaclass=SingletonMeta):
    async def send_pair_reqeust(self, request: DevicePairRequest) -> None:
        if await self.get_device_owner(device_id=request.device.id):
            raise DeviceAlreadyHasOwnerHTTPException(status_code=HTTPStatus.BAD_REQUEST, message="This device already has owner, so pair request cannot be sent")

        await _pair_manager.send_pair_request(request)

    async def get_pair_request(self, request_uuid: str) -> DevicePairRequest:
        return _pair_manager.get_request_by_uuid(request_uuid=request_uuid)

    async def accept_pair_request(self, request: DevicePairRequest) -> None:
        await _pair_manager.accept_pair_request(request.uuid)

    async def reject_pair_request(self, request: DevicePairRequest) -> None:
        await _pair_manager.reject_pair_request(request.uuid)

    async def get_pair_requests(self, *, device_id: int, timeout: Optional[int] = None) -> List[DevicePairRequest]:
        return await _pair_manager.get_pair_requests(device_id, timeout)

    async def get_device_owner(self, device_id: int) -> Optional[UserInternal]:
        user_model = await _device_pair_resource.get_owner(device_id=device_id)
        return None if user_model is None else user_model.to_schema(UserInternal)

    async def get_devices(self, user: UserInternal) -> List[UserInternal]:
        if user.is_device:
            return []

        models = await _device_pair_resource.get_user_devices(user.id)
        return list(map(lambda x: x.to_schema(UserInternal), models))

import asyncio
import logging
from typing import Optional, List

from src.core.state import project_settings
from src.core.utils.async_tools import call_after
from src.core.utils.collections import AsyncObservableDict
from src.core.utils.errors import supress_exception
from src.core.utils.singleton import SingletonMeta
from src.main.components.devices.models.device_pair_request import DevicePairRequest, DevicePairReqeustState
from src.main.components.devices.resources import DevicePairResourceST
from src.main.exceptions import NotFoundHTTPException

_logger = logging.getLogger(__name__)
_device_pair_resource = DevicePairResourceST()


class DevicePairRequestManagerST(metaclass=SingletonMeta):
    def __init__(self) -> None:
        self._pending_requests: AsyncObservableDict[str, DevicePairRequest] = AsyncObservableDict()

    def _change_request_state(self, request: DevicePairRequest, new_state: DevicePairReqeustState) -> None:
        request.state = new_state
        self._pending_requests.pop(request.uuid, None)

    async def _reject_request(self, request: DevicePairRequest):
        if request.state != DevicePairReqeustState.PENDING:
            return

        self._change_request_state(request, DevicePairReqeustState.REJECTED)

    async def _accept_request(self, request: DevicePairRequest) -> None:
        if request.state != DevicePairReqeustState.PENDING:
            return

        self._change_request_state(request, DevicePairReqeustState.ACCEPTED)

        await _device_pair_resource.create_device_pair(request.user, request.device)

    async def _auto_reject_after(self, request: DevicePairRequest, *, after: float) -> None:
        await call_after(self._reject_request(request), after=after)

    def get_request_by_uuid(self, request_uuid: str) -> DevicePairRequest:
        request = self._pending_requests.get(request_uuid)

        if request is None:
            raise NotFoundHTTPException(message=f"Request {request_uuid} was not found")

        return request

    async def get_pair_requests(self, device_id: int, timeout: Optional[int] = None) -> List[DevicePairRequest]:
        requests = [request for request in self._pending_requests.values() if request.device.id == device_id]

        if requests:
            return requests

        with supress_exception(asyncio.TimeoutError):
            requests.append(
                await self._pending_requests.wait_for(
                    filter_func=lambda x: x.device.id == device_id,
                    timeout=timeout
                )
            )
        return requests

    async def send_pair_request(self, request: DevicePairRequest) -> None:
        self._pending_requests[request.uuid] = request
        await self._auto_reject_after(request, after=project_settings.DEVICE_PAIR_REQUEST_TTL)

    async def accept_pair_request(self, request_uuid: str) -> None:
        request = self.get_request_by_uuid(request_uuid)
        await self._accept_request(request)

    async def reject_pair_request(self, request_uuid: str) -> None:
        request = self.get_request_by_uuid(request_uuid)
        await self._reject_request(request)

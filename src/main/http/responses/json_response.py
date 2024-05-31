from typing import TypeVar

from fastapi.responses import JSONResponse

from src.main.models import ApplicationResponsePayload

_contentT = TypeVar("_contentT")


class ApplicationJsonResponse(JSONResponse):
    def __init__(self, *, content: ApplicationResponsePayload[_contentT], **kwargs) -> None:
        super().__init__(content, **kwargs)

    def render(self, content: ApplicationResponsePayload[_contentT]) -> bytes:
        return content.model_dump_json().encode(self.charset)

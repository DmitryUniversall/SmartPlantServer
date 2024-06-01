from starlette.exceptions import HTTPException
from starlette.requests import Request

from src.core.exceptions import AbstractErrorHandler
from src.core.state import project_settings
from src.core.utils.types import JsonDict
from src.main.http.responses import ApplicationJsonResponse
from src.main.models import ApplicationResponsePayload


@AbstractErrorHandler.as_error_handler(exception_cls=HTTPException)
async def http_exception_handler(_: Request, error: HTTPException, **__) -> ApplicationJsonResponse:
    return ApplicationJsonResponse(
        content=ApplicationResponsePayload[JsonDict](
            ok=200 <= error.status_code < 300,
            application_status_code=project_settings.APPLICATION_STATUS_CODES.NOT_SPECIFIED,
            message=str(error),
            data={
                "detail": error.detail
            }
        ),
        status_code=error.status_code,
        headers=error.headers
    )

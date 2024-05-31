from src.core.exceptions import AbstractErrorHandler
from src.core.state import project_settings
from src.main.http.responses import ApplicationJsonResponse
from src.main.models import ApplicationResponsePayload


@AbstractErrorHandler.as_error_handler(exception_cls=Exception)
async def unknown_exception_handler(*_, **__) -> ApplicationJsonResponse:
    return ApplicationJsonResponse(
        content=ApplicationResponsePayload(
            ok=False,
            data=None,
            **project_settings.APPLICATION_STATUS_CODES.GENERIC_ERRORS.INTERNAL_SERVER_ERROR,
        ),
        status_code=500
    )

from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from starlette.requests import Request

from src.core.exceptions import AbstractErrorHandler
from src.core.state import project_settings
from src.core.utils.types import JsonObject
from src.main.http.responses import ApplicationJsonResponse
from src.main.models import ApplicationResponsePayload


@AbstractErrorHandler.as_error_handler(exception_cls=RequestValidationError)
async def http_validation_exception_handler(_: Request, exc: RequestValidationError, **__) -> ApplicationJsonResponse[JsonObject]:
    return ApplicationJsonResponse[JsonObject](
        content=ApplicationResponsePayload[JsonObject](
            ok=False,
            data={"detail": jsonable_encoder(exc.errors())},
            **project_settings.APPLICATION_STATUS_CODES.GENERIC_ERRORS.UNPROCESSABLE_ENTITY
        ),
        status_code=422
    )

# @AbstractErrorHandler.as_error_handler(exception_cls=WebSocketRequestValidationError)  TODO
# async def request_validation_exception_handler(websocket: WebSocket, exc: WebSocketRequestValidationError, **__) -> CustomJsonResponse:
#     await websocket.close(
#         code=WS_1008_POLICY_VIOLATION, reason=jsonable_encoder(exc.errors())
#     )
#
#     return CustomJsonResponse(
#         **project_settings.APPLICATION_STATUS_CODES.GENERIC_ERRORS.UNPROCESSABLE_ENTITY,
#         status_code=422,
#         content={"errors": jsonable_encoder(exc.errors())}
#     )
#
#
# async def websocket_request_validation_exception_handler(
#         websocket: WebSocket, exc: WebSocketRequestValidationError
# ) -> None:
#     await websocket.close(
#         code=WS_1008_POLICY_VIOLATION, reason=jsonable_encoder(exc.errors())
#     )

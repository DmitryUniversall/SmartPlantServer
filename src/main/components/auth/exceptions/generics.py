from src.core.state import project_settings
from src.main.models import ApplicationResponsePayload
from .base import AuthHTTPException


class AuthorizationNotSpecifiedHTTPException(AuthHTTPException):
    def get_default_response_payload(self) -> ApplicationResponsePayload:
        return ApplicationResponsePayload(
            ok=False,
            **project_settings.APPLICATION_STATUS_CODES.AUTH.AUTHORIZATION_NOT_SPECIFIED
        )


class AuthorizationInvalidHTTPException(AuthHTTPException):
    def get_default_response_payload(self) -> ApplicationResponsePayload:
        return ApplicationResponsePayload(
            ok=False,
            **project_settings.APPLICATION_STATUS_CODES.AUTH.AUTHORIZATION_INVALID
        )


class AuthorizationTypeUnknownHTTPException(AuthHTTPException):
    def get_default_response_payload(self) -> ApplicationResponsePayload:
        return ApplicationResponsePayload(
            ok=False,
            **project_settings.APPLICATION_STATUS_CODES.AUTH.AUTHORIZATION_TYPE_UNKNOWN
        )


class TokenNotSpecifiedHTTPException(AuthHTTPException):
    def get_default_response_payload(self) -> ApplicationResponsePayload:
        return ApplicationResponsePayload(
            ok=False,
            **project_settings.APPLICATION_STATUS_CODES.AUTH.TOKEN_NOT_SPECIFIED
        )


class TokenExpiredHTTPException(AuthHTTPException):
    def get_default_response_payload(self) -> ApplicationResponsePayload:
        return ApplicationResponsePayload(
            ok=False,
            **project_settings.APPLICATION_STATUS_CODES.AUTH.TOKEN_EXPIRED
        )


class TokenInvalidHTTPException(AuthHTTPException):
    def get_default_response_payload(self) -> ApplicationResponsePayload:
        return ApplicationResponsePayload(
            ok=False,
            **project_settings.APPLICATION_STATUS_CODES.AUTH.TOKEN_INVALID
        )


class TokenValidationFailed(AuthHTTPException):
    def get_default_response_payload(self) -> ApplicationResponsePayload:
        return ApplicationResponsePayload(
            ok=False,
            **project_settings.APPLICATION_STATUS_CODES.AUTH.TOKEN_VALIDATION_FAILED
        )


class AuthUserUnknownHTTPException(AuthHTTPException):
    def get_default_response_payload(self) -> ApplicationResponsePayload:
        return ApplicationResponsePayload(
            ok=False,
            **project_settings.APPLICATION_STATUS_CODES.AUTH.UNKNOWN_USER
        )


class AuthUserAlreadyExists(AuthHTTPException):
    def get_default_response_payload(self) -> ApplicationResponsePayload:
        return ApplicationResponsePayload(
            ok=False,
            **project_settings.APPLICATION_STATUS_CODES.GENERIC_ERRORS.ALREADY_EXISTS
        )


class WrongAuthCredentialsHTTPException(AuthHTTPException):
    def get_default_response_payload(self) -> ApplicationResponsePayload:
        return ApplicationResponsePayload(
            ok=False,
            **project_settings.APPLICATION_STATUS_CODES.AUTH.WRONG_AUTH_CREDENTIALS
        )

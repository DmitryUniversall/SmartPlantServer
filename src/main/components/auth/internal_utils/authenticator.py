import logging
from http import HTTPStatus
from typing import Tuple

import jwt
import pydantic

from src.core.utils.singleton import SingletonMeta
from src.core.utils.types import JsonDict
from src.main.components.auth.exceptions import (
    TokenExpiredHTTPException,
    TokenInvalidHTTPException,
    TokenValidationFailed,
    AuthUserUnknownHTTPException,
    WrongAuthCredentialsHTTPException,
    AuthUserAlreadyExists
)
from src.main.components.auth.internal_utils.jwt import decode_jwt_token, create_jwt_token
from src.main.components.auth.models.access_token_payload import AccessTokenPayload
from src.main.components.auth.models.refresh_token_payload import RefreshTokenPayload
from src.main.components.auth.resources.user_resource import UserResourceST
from src.main.db import UniqueConstraintFailed
from .session_manager_redis import AuthSessionManagerRedisST
from ..models.auth_token_pair import AuthTokenPair
from ..models.auth_token_payload import AuthTokenPayload
from ..models.user import UserModel, UserInternal

_logger = logging.getLogger(__name__)
_user_resource = UserResourceST()
_session_manager = AuthSessionManagerRedisST()


class JWTAuthenticatorST(metaclass=SingletonMeta):
    def _decode_token(self, token: str) -> JsonDict:
        try:
            return decode_jwt_token(token)
        except jwt.ExpiredSignatureError as error:
            raise TokenExpiredHTTPException(status_code=HTTPStatus.UNAUTHORIZED) from error
        except jwt.PyJWTError as error:
            raise TokenInvalidHTTPException(status_code=HTTPStatus.UNAUTHORIZED) from error

    def _decode_access_token(self, token: str) -> AccessTokenPayload:
        try:
            return AccessTokenPayload(**self._decode_token(token))
        except pydantic.ValidationError as error:
            raise TokenInvalidHTTPException(status_code=HTTPStatus.UNAUTHORIZED) from error

    def _decode_refresh_token(self, token: str) -> RefreshTokenPayload:
        try:
            return RefreshTokenPayload(**self._decode_token(token))
        except pydantic.ValidationError as error:
            raise TokenInvalidHTTPException(status_code=HTTPStatus.UNAUTHORIZED) from error

    async def _create_access_token(self, *, payload: AccessTokenPayload) -> str:
        await _session_manager.set_active_access_uuid(payload.user_id, payload.uuid)
        return create_jwt_token(payload=payload.to_json_dict(exclude='exp'), exp=payload.exp.timestamp())

    async def _create_refresh_token(self, *, payload: RefreshTokenPayload) -> str:
        await _session_manager.set_active_refresh_uuid(payload.user_id, payload.uuid)
        return create_jwt_token(payload=payload.to_json_dict(exclude='exp'), exp=payload.exp.timestamp())

    async def _get_user_from_token_payload(self, payload: AuthTokenPayload) -> UserInternal:
        try:
            user_model = await _user_resource.get_by_id(payload.user_id)
            return user_model.to_schema(scheme_cls=UserInternal)
        except UserModel.DoesNotExist as error:
            raise AuthUserUnknownHTTPException(status_code=HTTPStatus.UNAUTHORIZED) from error

    async def _create_token_pair(self, user: UserInternal) -> AuthTokenPair:
        access_payload = AccessTokenPayload(user_id=user.id)  # type: ignore
        refresh_payload = RefreshTokenPayload(user_id=user.id)  # type: ignore

        return AuthTokenPair(
            access_token=await self._create_access_token(payload=access_payload),
            refresh_token=await self._create_refresh_token(payload=refresh_payload)
        )

    async def _register_user(self, username: str, password: str, **field) -> UserInternal:
        try:
            user_model = await _user_resource.create_user(username, password, **field)
            return user_model.to_schema(scheme_cls=UserInternal)
        except UniqueConstraintFailed as error:
            raise AuthUserAlreadyExists(status_code=HTTPStatus.CONFLICT) from error

    async def _login_user(self, username: str, password: str, **fields) -> UserInternal:
        try:
            user_model = await _user_resource.get_by_username(
                username=username,
                password=_user_resource.hash_password(password),
                **fields
            )
            return user_model.to_schema(scheme_cls=UserInternal)
        except UserModel.DoesNotExist as error:
            raise WrongAuthCredentialsHTTPException(status_code=HTTPStatus.UNAUTHORIZED) from error

    async def _validate_access_token(self, payload: AccessTokenPayload) -> None:
        if not (await _session_manager.is_active_access(payload.user_id, payload.uuid)):
            raise TokenValidationFailed(status_code=HTTPStatus.UNAUTHORIZED)

    async def _verify_refresh_token(self, payload: RefreshTokenPayload) -> None:
        if not (await _session_manager.is_active_refresh(payload.user_id, payload.uuid)):
            raise TokenValidationFailed(status_code=HTTPStatus.UNAUTHORIZED)

    async def authenticate(self, access_token: str) -> UserInternal:
        payload = self._decode_access_token(access_token)
        await self._validate_access_token(payload)

        return await self._get_user_from_token_payload(payload)

    async def refresh(self, refresh_token: str) -> Tuple[UserInternal, AuthTokenPair]:
        payload = self._decode_refresh_token(refresh_token)
        await self._verify_refresh_token(payload)

        user = await self._get_user_from_token_payload(payload)
        return user, await self._create_token_pair(user)

    async def register(self, username: str, password: str, **fields) -> Tuple[UserInternal, AuthTokenPair]:
        user = await self._register_user(username, password, **fields)
        return user, await self._create_token_pair(user)

    async def login(self, username: str, password: str, **fields) -> Tuple[UserInternal, AuthTokenPair]:
        user = await self._login_user(username, password, **fields)
        return user, await self._create_token_pair(user)

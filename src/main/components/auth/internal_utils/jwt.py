from typing import Dict, Any, Union

import jwt

from src.core.state import project_settings
from src.core.utils.types import JsonDict


def create_jwt_token(*, payload: JsonDict, exp: Union[int, float]) -> str:
    encoded_jwt = jwt.encode(
        payload={
            "exp": exp,
            **payload
        },
        key=project_settings.SECRET_KEY,
        algorithm=project_settings.TOKEN_ENCRYPTION_ALGORITHM
    )

    return encoded_jwt


def decode_jwt_token(token: str) -> Dict[str, Any]:
    return jwt.decode(
        jwt=token,
        key=project_settings.SECRET_KEY,
        algorithms=[project_settings.TOKEN_ENCRYPTION_ALGORITHM]
    )

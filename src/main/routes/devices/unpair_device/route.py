# from fastapi import Depends
#
# from src.main.components.auth.models.user import UserInternal
# from src.main.components.auth.repository import AuthRepositoryST
# from src.main.components.auth.utils.dependencies.http_auth import HTTPJWTBearerAuthDependency
# from src.main.components.devices.repository.devices_repository import DevicesRepositoryST
# from src.main.http import ApplicationJsonResponse
# from ..router import devices_router
#
# _jwt_auth = HTTPJWTBearerAuthDependency()
# _auth_repository = AuthRepositoryST()
# _devices_repository = DevicesRepositoryST()
#
#
# @devices_router.post("/unpair/")
# async def pair_requests_get_route(user: UserInternal = Depends(_jwt_auth)) -> ApplicationJsonResponse:
#     pass

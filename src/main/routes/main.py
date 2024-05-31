from fastapi import APIRouter

from src.main.http import ApplicationResponseApiRoute
from .auth import auth_router
from .devices import devices_router
from .storage import storage_router

# Make sure that all endpoints implement base server interface
assert auth_router.route_class is ApplicationResponseApiRoute
assert devices_router.route_class is ApplicationResponseApiRoute
assert storage_router.route_class is ApplicationResponseApiRoute

main_router = APIRouter()
main_router.include_router(auth_router, prefix="/auth")
main_router.include_router(devices_router, prefix="/devices")
main_router.include_router(storage_router, prefix="/storage")

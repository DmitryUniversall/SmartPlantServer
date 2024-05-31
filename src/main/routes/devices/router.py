from fastapi import APIRouter

from src.main.http import ApplicationResponseApiRoute

devices_router = APIRouter(route_class=ApplicationResponseApiRoute)

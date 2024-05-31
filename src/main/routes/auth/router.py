from fastapi import APIRouter

from src.main.http import ApplicationResponseApiRoute

auth_router = APIRouter(route_class=ApplicationResponseApiRoute)

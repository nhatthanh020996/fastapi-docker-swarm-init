from fastapi import APIRouter

from app.core.auth.routers import auth_router

v1_router = APIRouter(prefix="/api/v1", tags=['V1'])

v1_router.include_router(auth_router)
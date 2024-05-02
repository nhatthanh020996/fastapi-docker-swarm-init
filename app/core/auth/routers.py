from contextlib import asynccontextmanager

from fastapi import Depends, APIRouter

from .schemas import UserCreate, UserRead, UserUpdate
from . import (
    SECRET,
    auth_backend,
    current_active_user,
    fastapi_users
)
from .models import User


auth_router = APIRouter(prefix='/auth', tags=["auth"])

auth_router.include_router(
    fastapi_users.get_auth_router(auth_backend), prefix="/jwt", tags=["auth"]
)

auth_router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)

auth_router.include_router(
    fastapi_users.get_reset_password_router(),
)

auth_router.include_router(
    fastapi_users.get_verify_router(UserRead),
)

auth_router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)


@auth_router.get("/authenticated-route")
async def authenticated_route(user: User = Depends(current_active_user)):
    return {"message": f"Hello {user.email}!"}

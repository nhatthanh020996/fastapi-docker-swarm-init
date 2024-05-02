from typing import AsyncGenerator, List

from fastapi import Depends
from fastapi_users.db import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
    SQLAlchemyUserDatabase,
)
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, relationship, mapped_column
from sqlalchemy import String

from app import Base
from app.configs.database import get_async_session



class User(SQLAlchemyBaseUserTableUUID, Base):
    username: Mapped[str] = mapped_column(
        String(length=100), unique=True, nullable=False
    )

async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)

from typing import AsyncIterator, Annotated
import logging
import time

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import event
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine

from .. import Base
from .settings import settings

DATABASE_URL = str(settings.DATABASE_URI)
logger = logging.getLogger(__name__)


engine = create_async_engine(DATABASE_URL, echo=False, future=True, pool_size=8)

async_session_maker = async_sessionmaker(engine, expire_on_commit=False)



async def get_async_session() -> AsyncIterator[AsyncSession]:
    async with async_session_maker() as session:
        return session


ASession = Annotated[AsyncSession, Depends(get_async_session)]


async def create_db_and_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


# if settings.ENABLE_DEBUG_SLOW_QUERY:
#     @event.listens_for(Engine, "before_cursor_execute")
#     def before_cursor_execute(conn, cursor, statement,
#                             parameters, context, executemany):
#         conn.info.setdefault('query_start_time', []).append(time.time())


#     @event.listens_for(Engine, "after_cursor_execute")
#     def after_cursor_execute(conn, cursor, statement,
#                             parameters, context, executemany):
#         total = time.time() - conn.info['query_start_time'].pop(-1)
#         if total > 0.2:
#             logger.warning("SQL query take too slow :(", extra={'query': statement, 'params': parameters, 'time-execution': total})

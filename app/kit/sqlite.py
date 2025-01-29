from collections.abc import AsyncGenerator
from typing import Literal, TypeAlias

from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncEngine, async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from app.settings import settings

ProcessName: TypeAlias = Literal["app", "worker"]


def create_async_engine(process_name: ProcessName) -> AsyncEngine:
    # application_name = f"{settings.ENV.value}.{process_name}"
    # connect_args = {"server_settings": {"application_name": application_name}}
    return _create_async_engine(
        str(settings.sqlite_dsn),
        echo=settings.DEBUG,
        # connect_args=connect_args if application_name else {},
    )


AsyncSessionMaker = async_sessionmaker[AsyncSession]


def create_async_sessionmaker(engine: AsyncEngine) -> async_sessionmaker[AsyncSession]:
    return async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)


async def get_async_db_sessionmaker(
    request: Request,
) -> AsyncGenerator[AsyncSessionMaker, None]:
    asyncsessionmaker: AsyncSessionMaker = request.state.asyncsessionmaker
    yield asyncsessionmaker


async def get_async_db_session(
    request: Request,
    asyncsessionmaker: AsyncSessionMaker = Depends(get_async_db_sessionmaker),
) -> AsyncGenerator[AsyncSession, None]:
    async with asyncsessionmaker() as asyncsession:
        try:
            request.state.asyncsession = asyncsession
            yield asyncsession
        except:
            await asyncsession.rollback()
            raise
        else:
            await asyncsession.commit()


__all__ = [
    "AsyncSession",
    "AsyncSessionMaker",
    "create_async_engine",
    "create_async_sessionmaker",
    "get_async_db_sessionmaker",
    "get_async_db_session",
]

import logging
from typing import List

from sqlalchemy import exc, select, update, desc, text, func
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio.engine import AsyncEngine


from database.db import (
    User, Config
)

logger = logging.getLogger(__name__)


class Repo:
    """Db abstraction layer"""

    def __init__(self, engine: AsyncEngine) -> None:
        self.engine = engine

    # Config
    async def get_config_parameters(self):
        async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        async with async_session() as session:
            stmt = select(Config).where(Config.id == 1)
            result = await session.execute(stmt)
            result = result.first()
            await session.commit()
        return result

    async def create_config(self, admins_ids: list, doc_ids: list) -> None:
        async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        async with async_session() as session:
            new_str = str(admins_ids)[1:-1]
            new_docs = str(doc_ids)[1:-1]
            session.add(Config(id=1, admins_ids=new_str, doc_ids=new_docs))
            await session.commit()
        return

    async def update_admin_ids(self, admins_ids: list) -> None:
        async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        async with async_session() as session:
            new_str = str(admins_ids)[1:-1]
            stmt = update(Config).where(
                Config.id == 1).values(admins_ids=new_str)
            await session.execute(stmt)
            await session.commit()
        return

    # User
    async def get_user_username(self, user_id: int):
        async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        async with async_session() as session:
            stmt = select(User.username, User.first_name).where(
                User.user_id == user_id)
            result = await session.execute(stmt)
            result = result.first()
            await session.commit()
        return result

    async def add_user(self, user_id: int, username: str, first_name=None) -> None:
        async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        async with async_session() as session:
            try:
                session.add(
                    User(user_id=user_id, username=username, first_name=first_name))
                await session.commit()
            except exc.IntegrityError:
                await session.rollback()
        return

    async def update_user_status(self, user_id: int, new_status: bool) -> None:
        async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        async with async_session() as session:
            stmt = update(User).where(User.user_id ==
                                      user_id).values(is_blocked=new_status)
            await session.execute(stmt)
            await session.commit()
        return

    async def update_user_firstname(self, user_id: int, new_firstname: str) -> None:
        async_session = async_sessionmaker(self.engine, expire_on_commit=False)
        async with async_session() as session:
            stmt = update(User).where(User.user_id == user_id).values(
                first_name=new_firstname)
            await session.execute(stmt)
            await session.commit()
        return

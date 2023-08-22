from typing import Type

from app.database.db import async_session_maker
from app.repositories.users import UsersRepository
from app.models import User
from fastapi import Depends


class UnitOfWork:
    users: Type[UsersRepository]

    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        from app.utils.dependency import get_current_user
        self.current_user = Depends(get_current_user)
        self.users = UsersRepository(self.session, model=User, current_user=self.current_user)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
        
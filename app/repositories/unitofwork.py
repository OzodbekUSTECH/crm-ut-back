from typing import Type

from app.database.db import async_session_maker
from app.repositories.users import UsersRepository
from app.models import User


class UnitOfWork:
    users: Type[UsersRepository]

    def __init__(self, current_user):
        self.session_factory = async_session_maker
        self.current_user = current_user
        
    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = UsersRepository(self.session, model=User, current_user=self.current_user)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
        
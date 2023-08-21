from abc import ABC, abstractmethod
from typing import Type

from app.database.db import async_session_maker
from app.repositories.users import UsersRepository
from app.models import User



class UnitOfWork:
    users: Type[UsersRepository]

    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        self.db = self.session.begin()
        self.users = UsersRepository(self.db, model=User)

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
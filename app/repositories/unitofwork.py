from abc import ABC, abstractmethod
from typing import Type

from app.database.db import get_async_session, async_session_maker
from app.repositories.users import UsersRepository
from app.services.users import UsersService
from app.models import User


from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/users/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
):
    return await UsersService().get_current_user(token)

class UnitOfWork:
    users: Type[UsersRepository]

    def __init__(self):
        self.session_factory = async_session_maker

    async def __aenter__(self):
        self.session = self.session_factory()
        self.users = UsersRepository(self.session, model=User, current_user=Depends(get_current_user))

    async def __aexit__(self, *args):
        await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
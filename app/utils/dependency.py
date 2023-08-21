from app.models import User

from app.repositories.users import UsersRepository
from app.services.users import UsersService
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.db import get_async_session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.repositories.unitofwork import UnitOfWork


#services dependencies
async def get_users_services(db: AsyncSession = Depends(get_async_session)):
    pass
    # return UsersService(UsersRepository(session=db, model=User))

# Создание сервиса пользователей с передачей UnitOfWork
users_services = UsersService(UnitOfWork())







oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/users/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
):
    return await users_services.get_current_user(token)



class RoleChecker:
    def __init__(self, roles: list[str]):
        self.allowed_roles = roles

    def __call__(self, current_user = Depends(get_current_user)):
        if current_user.role not in self.allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied. Insufficient privileges."
            )
        return True
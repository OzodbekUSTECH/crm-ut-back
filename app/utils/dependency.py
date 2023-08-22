from app.models import User
from typing import Annotated
from app.repositories.users import UsersRepository
from app.services.users import UsersService

from app.database.db import  async_session_maker

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordBearer
# from app.repositories.unitofwork import UnitOfWork

#services dependencies
from typing import Type




# async def get_users_services(db: Session = Depends(get_async_session)):
#     # return UsersService(UsersRepository(session=db, model=User))
#     pass
users_service = UsersService()







oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/users/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
):
    return await UsersService().get_current_user(token)



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
UOWDep = Annotated[UnitOfWork, Depends(UnitOfWork)]
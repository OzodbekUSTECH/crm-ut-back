# from app.models import User

from app.repositories.users import UsersRepository
from app.services.users import UsersService
from typing import Annotated

from app.database.db import get_async_session
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.repositories.unitofwork import UnitOfWork


#services dependencies
UOWDep = Annotated[UnitOfWork, Depends(UnitOfWork)]
# async def get_users_services(db: Session = Depends(get_async_session)):
#     return UsersService(UsersRepository(session=db, model=User))








oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/users/login")


async def get_current_user(
    uow: UOWDep,
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
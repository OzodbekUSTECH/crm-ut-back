from typing import Annotated
from app.services.users import UsersService


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.repositories.unitofwork import UnitOfWork


UOWDep = Annotated[UnitOfWork, Depends(UnitOfWork)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/users/login")


async def get_current_user(
    token: str = Depends(oauth2_scheme),
):
    return await UsersService().get_current_user(token)


async def get_users_service(uow: UOWDep, current_user = Depends(get_current_user)):
    return UsersService(uow, current_user=current_user)

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
from typing import Annotated
from app.services.users import UsersService


from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.repositories.unitofwork import UnitOfWork


UOWDep = Annotated[UnitOfWork, Depends(UnitOfWork)]
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/users/login")




async def get_users_service(uow: UOWDep):
    return UsersService(uow)

async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    user_service: Annotated[UsersService, Depends(get_users_service)]
):
    return await user_service.get_current_user(token)



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
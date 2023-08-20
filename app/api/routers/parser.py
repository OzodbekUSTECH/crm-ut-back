from typing import Annotated

from fastapi import APIRouter, Depends
from app.services.users import UsersService
from app.utils.dependency import get_users_services, get_current_user
from app.schemas.users import UserCreateSchema, UserSchema, UserUpdateSchema, TokenSchema, ResetPasswordSchema
from app.repositories.base import Pagination
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/parser",
    tags=["Parser"],
)

@router.post('/users')
async def parse_all_users(
    url: str,
    users_service: Annotated[UsersService, Depends(get_users_services)]
):
    return await users_service.parse_all_users(url)
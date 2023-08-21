from typing import Annotated

from fastapi import APIRouter, Depends
from app.services.users import UsersService
from app.utils.dependency import get_current_user, users_service
from app.schemas.users import UserCreateSchema, UserSchema, UserUpdateSchema, TokenSchema, ResetPasswordSchema
from app.repositories.base import Pagination
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(
    prefix="/users",
    tags=["Users"],
)


@router.post('', name="Registration", response_model=UserSchema)
async def create_user(
    user_data: UserCreateSchema,
) -> UserSchema:
    """
    Create User:
    - return: User data.
    """
    return await users_service.register_user(user_data) 

@router.post('/login', name="get access token", response_model=TokenSchema)
async def login_in(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenSchema:
    """
    Get Access Token
    - param username: The email of the user.
    - param password: The password of the user.
    - return: Access Token and Type.
    """
    return await UsersService().authenticate_user(form_data.username, form_data.password)


@router.get('', name="get_all_users", response_model=list[UserSchema])
async def get_all_users_data(
    pagination: Annotated[Pagination, Depends()]
) -> list[UserSchema]:
    """
    Get All Users Data:
    - param page: The page.
    - param page_size: The quantity of users per page.
    - return: list of all users.
    """
    return await users_service.get_all_users(pagination)


@router.get('/me', name="get own user data", response_model=UserSchema)
async def get_own_user_data(
    current_user = Depends(get_current_user),
) -> UserSchema:
    """
    Get Own User Data
    - return: User data.
    """
    return current_user


@router.get('/{user_id}', name="get user by ID", response_model=UserSchema)
async def get_user_data_by_id(
    user_id: int
) -> UserSchema:
    """
    Get User By ID:
    - param user_id: The ID of the user to get.
    - return: User data.
    """
    return await UsersService().get_user_by_id(user_id)



@router.put('/{user_id}', name="Update User Data", response_model=UserSchema, dependencies=[Depends(get_current_user)])
async def update_user_data(
    user_id: int, 
    user_data: UserUpdateSchema,
) -> UserSchema:
    """
    Update User Data
    - param user_id: The ID of the user to update.
    - return: Updated user data.
    """
    return await users_service.update_user(user_id, user_data)


@router.delete('/{user_id}', name="delete user data", response_model=UserSchema)
async def delete_user_data(
    user_id: int,
) -> UserSchema:
    """
    Delete User:
    - param user_id: The id of the user to delete.
    - return: User data.
    """
    return await users_service.delete_user(user_id)

# @router.post('/forgot/password', tags=["Auth"], name="forgot password")
# async def forgot_password(
#     email: str, 
#     email_sender: EmailSender = Depends()
# ):
#     """
#     Forgot Password:
#     - return: Message success or error

#     :send a link to reset password to the email address.
#     """
#     return await email_sender.send_reset_password_link(email)

# @router.post('/reset/password', tags=["Auth"], name="reset password")
# async def reset_password(
#     token: str, 
#     user_password: ResetPasswordSchema,
#     users_service: Annotated[UsersService, Depends(get_users_services)]
# ):
#     """
#     Reset password:
#     - return: Message that password has been changed or something went wrong.
#     """
#     await users_service.reset_password(token, user_password.password1)

#     return {"message": "password has been changed successfully"}
















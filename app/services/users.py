from app.repositories.users import UsersRepository
from app.schemas.users import UserCreateSchema, UserUpdateSchema, UserSchema, TokenSchema, TokenData
from app.security.password import PasswordHandler
from app.security.jwthandler import JWTHandler
from app.repositories.base import Pagination
from fastapi import HTTPException, status
from datetime import timedelta
from jose import JWTError
from datetime import datetime
from app.utils.exceptions import CustomExceptions
import httpx
from app.repositories.unitofwork import UnitOfWork
from fastapi import Depends
from typing import Annotated

class UsersService:
    uow = UnitOfWork()
    # def __init__(self, uow: UnitOfWork):
    #     self.uow = uow

    async def register_user(self, user_data: UserCreateSchema) -> UserSchema:
        async with self.uow:
            existing_user = await self.uow.users.get_by_email(user_data.email)
            if existing_user:
                raise CustomExceptions.conflict("Already exists user with this email")

            hashed_password = PasswordHandler.hash(user_data.password)

            user_dict = {
                "email": user_data.email,
                "password": hashed_password
            }
            created_user = await self.uow.users.create_one(user_dict)
            await self.uow.commit()
            return created_user
        
    async def get_all_users(self, pagination: Pagination) -> list[UserSchema]:
        async with self.uow:
            return await self.uow.users.get_all(pagination)

    async def get_user_by_id(self, uow: UnitOfWork, user_id: int):
        async with uow:
            user = await uow.users.get_by_id(user_id)
            await uow.commit()
            return user

    async def update_user(self, user_id: int, user_data: UserUpdateSchema) -> UserSchema:
        user_dict = user_data.model_dump()
        async with self.uow:
            updated_user = await self.uow.users.update_one(user_id, user_dict)
            await self.uow.commit()
            return updated_user


    async def delete_user(self, user_id: int) -> UserSchema:
        async with self.uow:
            deleted_user = await self.uow.users.delete_one(user_id)
            await self.uow.commit()
            return deleted_user

    async def authenticate_user(self, email: str, password: str) -> TokenSchema:
        async with self.uow:
            user = await self.uow.users.get_by_email(email)
                
            if not user or not PasswordHandler.verify(password, user.password):
                raise CustomExceptions.unauthorized("Incorrect email or password")

            access_token_expires = timedelta(minutes=JWTHandler.ACCESS_TOKEN_EXPIRE_MINUTES)

            access_token = await JWTHandler.create_access_token(
                data={"id": user.id, "email": user.email}, expires_delta=access_token_expires
            )
            return TokenSchema(access_token=access_token, token_type="Bearer")

    
    
    async def get_current_user(self, token: str) -> UserSchema:
        credentials_exception = CustomExceptions.unauthorized("Could not validate credentials")
        try:
            payload = await JWTHandler.decode(token)
            email: str = payload.get("email")  # "sub" is the key used by JWT to represent the subject (usually user ID or email)
            if email is None:
                raise credentials_exception
            token_data = TokenData(email=email)
        except JWTError:
            raise credentials_exception
        
        async with self.uow:

            user = await self.uow.users.get_by_email(token_data.email)
            
            if user is None:
                raise credentials_exception

            return user

    
    
    async def generate_reset_token(self, email: str) -> str:
        payload = {
            "email": email,
            "exp": datetime.utcnow() + timedelta(hours=2)
        }
        token = await JWTHandler.encode(payload)
        return token
    
    async def reset_password(self, token: str, password: str) -> UserSchema:
        user = await self.get_current_user(token)
        hashed_password = PasswordHandler.hash(password)
        password_dict = {
            "password": hashed_password
        }
        async with self.uow:
            user_instance = await self.uow.users.update_one(user.id, password_dict)
            await self.uow.commit()
            return user_instance

    
    # async def parse_all_users(self, url: str):
    #     async with httpx.AsyncClient() as client:
    #         response = await client.get(url)
    #         response.raise_for_status()
    #         users = response.json()

    #         for user_data in users:
    #             user_dict = {
    #                 "email": user_data.get("email", user_data.get("mail", user_data.get("email_address", None))),
    #                 "password": "$2b$12$1c31RxAswu2qzs7l.erkbO2ucuj6mSv7Ncv3dDB5WYkIdERHz87i.",
    #             }
    #             await self.users_repo.create_one(user_dict)

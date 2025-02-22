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
from app.models import User
import httpx
from app.repositories.unitofwork import UnitOfWork
from app.utils.permissions import has_permission

class UsersService:
    def __init__(self, uow: UnitOfWork):
        self.uow = uow
        

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
            users = await self.uow.users.get_all(pagination)
            return [user[0].to_read_model() for user in users]

    async def get_user_by_id(self, user_id: int):
        async with self.uow:
            user = await self.uow.users.get_by_id(user_id)
            return user.to_read_model()

    async def update_user(
            self, 
            user_id: int, 
            user_data: UserUpdateSchema,
            current_user: User
        ) -> UserSchema:
        await has_permission.is_id_belongs_to_current_user(user_id, current_user)
        user_dict = user_data.model_dump()
        async with self.uow:
            existing_user = await self.uow.users.get_by_email(user_data.email)
            if existing_user:
                raise CustomExceptions.conflict("Already exists user with this email")

            updated_user = await self.uow.users.update_one(user_id, user_dict)
            await self.uow.commit()
            return updated_user


    async def delete_user(self, user_id: int, current_user: User) -> UserSchema:
        await has_permission.is_id_belongs_to_current_user(user_id, current_user)

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
            user_id: int = payload.get("id")  
            if user_id is None:
                raise credentials_exception
            token_data = TokenData(id=user_id)
        except JWTError:
            raise credentials_exception
        
        async with self.uow:
            user = await self.uow.users.get_by_id(token_data.id)
            
            if user is None:
                raise credentials_exception

            return user.to_read_model()

    
    
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

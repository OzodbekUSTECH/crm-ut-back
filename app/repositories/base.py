from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.declarative import DeclarativeMeta
from fastapi import Query
from sqlalchemy import insert, select, update, delete
from app.models import User
from fastapi import Depends


class Pagination:
    def __init__(self, page: int = Query(1, ge=1), page_size: int = Query(100, le=100)):
        self.page = page
        self.page_size = page_size
    
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size
        
    @property
    def limit(self) -> int:
        return self.page_size



class BaseRepository:
    """
    Dont use 'to_read_model()' method in order to get full info of model despite the schema
    and also use any information in services
    """
    def __init__(self, session: AsyncSession, model:DeclarativeMeta):
        self.session = session
        self.model = model

    async def create_one(self, data: dict) -> dict:
        stmt = insert(self.model).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_all(self, pagination: Pagination) -> list:
        stmt = select(self.model).order_by(self.model.id).offset(pagination.offset).limit(pagination.limit)
        result = await self.session.execute(stmt)
        return result.all()

    async def get_by_id(self, id: int) -> dict:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> dict:
        stmt = select(self.model).where(self.model.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none() 

    async def update_one(self, id: int, data: dict) -> dict:
        stmt = update(self.model).where(self.model.id == id).values(**data).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()
    
    async def delete_one(self, id: int) -> dict:
        stmt = delete(self.model).where(self.model.id == id).returning(self.model)
        result = await self.session.execute(stmt)
        return result.scalar_one()
    
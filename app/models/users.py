from app.database.db import Base
from enum import Enum as PyEnum
from sqlalchemy import String, Boolean, BigInteger, Column, Integer, Enum, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.schemas.users import UserSchema
from app.utils.exceptions import CustomExceptions

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]

    created_at: Mapped[DateTime] = mapped_column(default=func.now())
    updated_at: Mapped[DateTime] = mapped_column(default=func.now, onupdate=func.now())

    def to_read_model(self):
        return UserSchema(
            **self.__dict__
        )
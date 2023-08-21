from app.database.db import Base
from enum import Enum as PyEnum
from sqlalchemy import String, Boolean, BigInteger, Column, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.schemas.users import UserSchema

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]

    def to_read_model(self):
        if self.id is None:
            return None
        return UserSchema(
            **self.__dict__
        )
from app.database.db import Base
from enum import Enum as PyEnum
from sqlalchemy import String, Boolean, BigInteger, Column, Integer, Enum, func, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from app.schemas.users import UserSchema
from app.utils.exceptions import CustomExceptions
from datetime import datetime
import pytz

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    password: Mapped[str]

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=datetime.now(tz=pytz.timezone('Asia/Tashkent'))
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=datetime.now(tz=pytz.timezone('Asia/Tashkent')), server_onupdate=datetime.now(tz=pytz.timezone('Asia/Tashkent')),
    )

    def to_read_model(self):
        return UserSchema(
            **self.__dict__
        )
from app.database.db import Base
from enum import Enum as PyEnum
from sqlalchemy import String, Boolean, BigInteger, Column, Integer, Enum
from sqlalchemy.orm import Mapped, mapped_column


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True)
    password = Column(String)

    
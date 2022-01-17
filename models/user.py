from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from config.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    # is_active = Column(Boolean, default=True)
    role = Column(String, default='user')


class UserBaseSchema(BaseModel):
    login: str
    role: str

    class Config:
        orm_mode = False


class UserCreateSchema(BaseModel):
    login: str
    password: str
    role: str

    class Config:
        orm_mode = False


class UserSchema(UserBaseSchema):
    id: int

    class Config:
        orm_mode = True

from pydantic import BaseModel
from sqlalchemy import Boolean, Column, Integer, String

from config.database import Base


class User(Base):
    """Usuario de aplicación.

    `is_active` implementa borrado lógico: False cuando el usuario se da de baja
    sin borrar la fila.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True, nullable=False)
    role = Column(String, default="user")


class UserBaseSchema(BaseModel):
    """UserBaseSchema Schema"""

    login: str
    role: str

    class Config:
        # pylint: disable=missing-class-docstring
        orm_mode = False


class UserCreateSchema(UserBaseSchema):
    """UserCreateSchema Schema"""

    password: str

    class Config:
        # pylint: disable=missing-class-docstring
        orm_mode = False


class UserSchema(UserBaseSchema):
    """UserSchema Schema"""

    id: int
    is_active: bool = True

    class Config:
        # pylint: disable=missing-class-docstring
        orm_mode = True

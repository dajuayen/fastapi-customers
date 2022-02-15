from typing import Optional

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from config.database import Base


class Customer(Base):
    """Customer Class"""
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    # is_active = Column(Boolean, default=True)
    photo = Column(String)


class CustomerBaseSchema(BaseModel):
    """CustomerBaseSchema Schema"""
    name: str
    surname: str

    class Config:
        # pylint: disable=missing-class-docstring
        orm_mode = True


class CustomerCreateSchema(BaseModel):
    """CustomerCreateSchema Schema"""
    name: str
    surname: str
    photo: Optional[str] = None

    class Config:
        # pylint: disable=missing-class-docstring
        orm_mode = True


class CustomerSchema(CustomerCreateSchema):
    """CustomerSchema Schema"""
    id: int

    class Config:
        # pylint: disable=missing-class-docstring
        orm_mode = True

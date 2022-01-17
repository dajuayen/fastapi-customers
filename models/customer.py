from typing import Optional, Union

from pydantic import BaseModel
from sqlalchemy import Column, Integer, String

from config.database import Base


class Customer(Base):
    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    # is_active = Column(Boolean, default=True)
    photo = Column(String)


class CustomerBaseSchema(BaseModel):
    name: str
    surname: str

    class Config:
        orm_mode = True


class CustomerCreateSchema(BaseModel):
    name: str
    surname: str
    photo: Optional[str] = None

    class Config:
        orm_mode = True


class CustomerSchema(CustomerCreateSchema):
    id: int

    class Config:
        orm_mode = True


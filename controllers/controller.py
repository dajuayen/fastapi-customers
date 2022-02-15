from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel
from sqlalchemy.orm import Session, Query

from config.database import Base


class Controller(ABC):
    """Controller Abstract Class"""
    query: Query

    @abstractmethod
    def __init__(self, session=Session, internal_class=Base):
        self.session = session
        self.in_cls = internal_class
        self.query = self.session.query(self.in_cls)

    def get(self, identifier: int):
        """ Get object by identifier
        Args:
            identifier: id int
        Returns: object
        """
        return self.query.filter_by(id=identifier).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        """ Get object list
        Args:
            skip: number of objects to skip to start the list (int)
            limit: limit of objects to return in the list (int)
        Returns: object list
        """
        return self.query.offset(skip).limit(limit).all()

    def delete(self, identifier: int) -> Any:
        """ Delete object
        Args:
            identifier: id (int)
        Returns: result statement
        """
        result = self.query.filter_by(id=identifier).delete()
        self.session.commit()
        return result

    @abstractmethod
    def create(self, schema: BaseModel) -> BaseModel:
        """ Create object
        Args:
            schema: Schema with the required fields of the class to create an
            object.
        Returns: Schema of the created object.
        """
        db_object = self.in_cls(**schema.dict())
        assert isinstance(db_object, self.in_cls)
        self.session.add(db_object)
        self.session.commit()
        self.session.refresh(db_object)
        return db_object

    @abstractmethod
    def update(self, schema: BaseModel):
        """ Update object
        Args:
            schema: Schema with the modifiable fields of the object.
        Returns: result statement.
        """
        result = self.query.filter_by(id=schema.id).update(schema.dict())
        self.session.commit()
        if result:
            return schema
        return result

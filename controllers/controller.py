from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel
from sqlalchemy.orm import Session, Query

from config.database import Base
from config.logger import logger


class Controller(ABC):
    """Controller Abstract Class"""

    query: Query

    @abstractmethod
    def __init__(self, session=Session, internal_class=Base):
        self.session = session
        self.in_cls = internal_class
        self.query = self.session.query(self.in_cls)

    def get(self, identifier: int):
        """Get object by identifier
        Args:
            identifier: id int
        Returns: object
        """
        return self.query.filter_by(id=identifier).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        """Get object list
        Args:
            skip: number of objects to skip to start the list (int)
            limit: limit of objects to return in the list (int)
        Returns: object list
        """
        return self.query.offset(skip).limit(limit).all()

    def delete(self, identifier: int) -> Any:
        """Delete object
        Args:
            identifier: id (int)
        Returns: result statement
        """
        logger.info("Eliminar %s id=%s", self.in_cls.__name__, identifier)
        result = self.query.filter_by(id=identifier).delete()
        self.session.commit()
        logger.info(
            "Eliminado %s id=%s filas=%s",
            self.in_cls.__name__,
            identifier,
            result,
        )
        return result

    @abstractmethod
    def create(self, schema: BaseModel) -> BaseModel:
        """Create object
        Args:
            schema: Schema with the required fields of the class to create an
            object.
        Returns: Schema of the created object.
        """
        logger.info("Crear %s", self.in_cls.__name__)
        db_object = self.in_cls(**schema.dict())
        assert isinstance(db_object, self.in_cls)
        self.session.add(db_object)
        self.session.commit()
        self.session.refresh(db_object)
        logger.info(
            "Creado %s id=%s",
            self.in_cls.__name__,
            getattr(db_object, "id", None),
        )
        return db_object

    @abstractmethod
    def update(self, schema: BaseModel):
        """Update object
        Args:
            schema: Schema with the modifiable fields of the object.
        Returns: result statement.
        """
        logger.info(
            "Actualizar %s id=%s",
            self.in_cls.__name__,
            getattr(schema, "id", None),
        )
        result = self.query.filter_by(id=schema.id).update(schema.dict())
        self.session.commit()
        logger.info(
            "Actualizado %s id=%s filas=%s",
            self.in_cls.__name__,
            schema.id,
            result,
        )
        if result:
            return schema
        return result

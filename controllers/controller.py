from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel
from sqlalchemy.orm import Session, Query

from config.database import Base


class Controller(ABC):
    q: Query

    @abstractmethod
    def __init__(self, session=Session, internal_class=Base):
        self.db = session
        self.in_cls = internal_class
        self.q = self.db.query(self.in_cls)

    def get(self, id: int):
        return self.q.filter_by(id=id).first()

    def get_all(self, skip: int = 0, limit: int = 100):
        return self.q.offset(skip).limit(limit).all()

    def delete(self, id: int) -> Any:
        result = self.q.filter_by(id=id).delete()
        self.db.commit()
        return result

    @abstractmethod
    def create(self, schema: BaseModel) -> BaseModel:
        db_object = self.in_cls(schema.dict())
        assert isinstance(db_object, self.in_cls)
        self.db.add(db_object)
        self.db.commit()
        self.db.refresh(db_object)
        return db_object

    @abstractmethod
    def update(self, schema: BaseModel):
        result = self.q.filter_by(id=schema.id).update(schema.dict())
        self.db.commit()
        if result:
            return schema
        return result

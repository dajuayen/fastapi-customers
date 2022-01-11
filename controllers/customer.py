from typing import List, Any

from sqlalchemy.orm import Session

from models.customer import Customer, CustomerBaseSchema, CustomerSchema, \
    CustomerCreateSchema


class CustomerController(object):

    def __init__(self, session=Session):
        self.db = session

    def get_all(self) -> List[Customer]:
        return self.db.query(Customer).order_by(Customer.id).all()

    def get_customers(self, skip: int = 0, limit: int = 100) -> List[Customer]:
        return self.db.query(Customer).offset(skip).limit(limit).all()

    def get_by_name_surname(self, customer: CustomerBaseSchema):
        return self.db.query(Customer).filter(
            Customer.name.like(customer.name),
            Customer.surname.like(customer.surname)
        ).first()

    def get(self, id: int):
        return self.db.query(Customer).filter(Customer.id == id).first()

    def create(self, customer: CustomerCreateSchema):
        db_user = Customer(**customer.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, customer: CustomerSchema):
        result = self.db.query(Customer).filter(
            Customer.id == customer.id).update(
            {'id': customer.id,
             'name': customer.name, 'surname': customer.surname,
             'photo': customer.photo})
        self.db.commit()
        if result:
            return customer
        return result

    def delete(self, id: int) -> Any:
        result = self.db.query(Customer).filter_by(id=id).delete()
        self.db.commit()
        return result

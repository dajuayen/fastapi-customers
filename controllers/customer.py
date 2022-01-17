from typing import List, Any

from sqlalchemy.orm import Session

from controllers.controller import Controller
from models.customer import Customer, CustomerBaseSchema, CustomerSchema, \
    CustomerCreateSchema


class CustomerController(Controller):

    def __init__(self, session=Session, internal_class=Customer):
        self.db = session
        self.in_cls = internal_class
        self.q = self.db.query(self.in_cls)

    def get_by_name_surname(self, customer: CustomerBaseSchema):
        return self.q.filter(
            Customer.name.like(customer.name),
            Customer.surname.like(customer.surname)
        ).first()

    def create(self, customer: CustomerCreateSchema):
        return super(CustomerController, self).create(customer)

    def update(self, customer: CustomerSchema):
        return super(CustomerController, self).update(customer)

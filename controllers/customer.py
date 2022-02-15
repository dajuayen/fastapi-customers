from sqlalchemy.orm import Session

from controllers.controller import Controller
from models.customer import Customer, CustomerBaseSchema, CustomerSchema, \
    CustomerCreateSchema


class CustomerController(Controller):
    """Customer Controller Class"""

    def __init__(self, session=Session, internal_class=Customer):
        super().__init__(session, internal_class)

    def get_by_name_surname(self, customer: CustomerBaseSchema):
        """ Get customer by name and surname.
        Args:
            customer: CustomerSchema
        Returns: Customer or None
        """
        return self.query.filter(
            Customer.name.like(customer.name),
            Customer.surname.like(customer.surname)
        ).first()

    def create(self, schema: CustomerCreateSchema):
        """ Create customer.
        Args:
            schema: CustomerSchema
        Returns: Customer or None
        """
        return super().create(schema)

    def update(self, schema: CustomerSchema):
        """ Update customer.
        Args:
            schema: CustomerSchema
        Returns: Customer or None
        """
        return super().update(schema)

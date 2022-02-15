from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from config.hasher import oauth2_scheme
from controllers.customer import CustomerController
from models.customer import CustomerSchema, CustomerCreateSchema

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
    dependencies=[Depends(oauth2_scheme)],
    responses={404: {"description": "Not found"}},
)


@router.get("/", response_model=List[CustomerSchema])
async def customers(session: Session = Depends(get_db)) -> List[CustomerSchema]:
    """ Get /customers
    Args:
        session: Session

    Returns: list
    """
    result = CustomerController(session).get_all()
    return [CustomerSchema.from_orm(customer) for customer in result]


@router.get("/{customer_id}", response_model=CustomerSchema)
async def read(customer_id: str,
               session: Session = Depends(get_db)) -> CustomerSchema:
    """ Get /customers/{customer_id}
    Args:
        customer_id: id (str)
        session: Session

    Returns: CustomerSchema
    """
    customer = CustomerController(session).get(int(customer_id))
    if not customer:
        raise HTTPException(status_code=404,
                            detail="Customer not Found")
    return customer


@router.put("/", response_model=CustomerSchema)
async def update(customer: CustomerSchema,
                 session: Session = Depends(get_db)) -> CustomerSchema:
    """ Put /customers
    Args:
        customer: CustomerSchema
        session: Session

    Returns: CustomerSchema
    """
    controller = CustomerController(session)
    customer_db = controller.get(customer.id)
    if not customer_db:
        raise HTTPException(status_code=404,
                            detail="Customer not Found")
    return controller.update(customer)


@router.post("/", response_model=CustomerSchema)
async def create(customer: CustomerCreateSchema,
                 session: Session = Depends(get_db)) -> CustomerSchema:
    """ Post /customers
    Args:
        customer: CustomerCreateSchema
        session: Session

    Returns:CustomerSchema
    """
    controller = CustomerController(session)
    customer_db = controller.get_by_name_surname(customer)
    if customer_db:
        raise HTTPException(status_code=400,
                            detail="Customer already registered")
    new_customer = controller.create(schema=customer)
    return CustomerSchema.from_orm(new_customer)


@router.delete("/{customer_id}")
def delete(customer_id: str, session: Session = Depends(get_db)):
    """ Delete /customer/{customer_id}
    Args:
        customer_id: id (str)
        session: Session

    Returns: result
    """
    controller = CustomerController(session)
    customer_db = controller.get(int(customer_id))
    if not customer_db:
        raise HTTPException(status_code=404,
                            detail="Customer not found")
    result = controller.delete(int(customer_id))
    return result

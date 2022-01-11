from fastapi import APIRouter
from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from config.database import get_db
from controllers.customer import CustomerController
from models.customer import CustomerSchema, CustomerCreateSchema

router = APIRouter(
    prefix="/customers",
    tags=["Customers"],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def customers(db: Session = Depends(get_db)):
    return CustomerController(db).get_all()


@router.get("/{customer_id}")
async def read(customer_id: str,
               db: Session = Depends(get_db)) -> CustomerSchema:
    customer = CustomerController(db).get(int(customer_id))
    if not customer:
        raise HTTPException(status_code=404,
                            detail="Customer not Found")
    return customer


@router.put("/", response_model=CustomerSchema)
async def update(customer: CustomerSchema,
                 db: Session = Depends(get_db)) -> CustomerSchema:
    controller = CustomerController(db)
    customer_db = controller.get(customer.id)
    if not customer_db:
        raise HTTPException(status_code=404,
                            detail="Customer not Found")
    return controller.update(customer)


@router.post("/", response_model=CustomerCreateSchema)
def create(customer: CustomerCreateSchema,
           db: Session = Depends(get_db)) -> CustomerSchema:
    controller = CustomerController(db)
    customer_db = controller.get_by_name_surname(customer)
    if customer_db:
        raise HTTPException(status_code=400,
                            detail="Customer already registered")
    new_customer = controller.create(customer=customer)
    return CustomerSchema.from_orm(new_customer)


@router.delete("/{customer_id}")
def delete(customer_id: str, db: Session = Depends(get_db)):
    controller = CustomerController(db)
    customer_db = controller.get(int(customer_id))
    if not customer_db:
        raise HTTPException(status_code=404,
                            detail="Customer not found")
    result = controller.delete(int(customer_id))
    return result

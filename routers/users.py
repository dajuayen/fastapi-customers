from typing import List

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from config.database import get_db
from controllers.security import get_current_user_permisions
from controllers.user import UserController
from models.user import User, UserSchema, UserCreateSchema

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_user_permisions)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def users(db: Session = Depends(get_db)) -> List[UserSchema]:
    list_users = [UserSchema.from_orm(db_user) for db_user in
                  UserController(db).get_all()]
    return list_users


@router.get("/{user_id}")
async def read(user_id: str,
               db: Session = Depends(get_db)) -> UserSchema:
    db_user = UserController(db).get(int(user_id))
    if not db_user:
        raise HTTPException(status_code=404,
                            detail="User not Found")
    schema_user = UserSchema.from_orm(db_user)
    return schema_user


@router.put("/", response_model=UserSchema)
async def update(user: UserSchema,
                 db: Session = Depends(get_db)) -> UserSchema:
    controller = UserController(db)
    customer_db = controller.get(user.id)
    if not customer_db:
        raise HTTPException(status_code=404,
                            detail="User not Found")
    return controller.update(user)


@router.post("/", response_model=UserCreateSchema)
def create(user: UserCreateSchema,
           db: Session = Depends(get_db)) -> UserSchema:
    controller = UserController(db)
    user_db = controller.get_by_login(user)
    if user_db:
        raise HTTPException(status_code=400,
                            detail="User already registered")
    new_user = controller.create(user=user)
    if new_user:
        HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Validation Error",
        )
    return UserSchema.from_orm(new_user)


@router.delete("/{user_id}")
def delete(user_id: str, db: Session = Depends(get_db)):
    controller = UserController(db)
    user_db = controller.get(int(user_id))
    if not user_db:
        raise HTTPException(status_code=404,
                            detail="User not found")
    result = controller.delete(int(user_id))
    return result

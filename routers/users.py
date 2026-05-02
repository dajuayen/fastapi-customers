from typing import List

from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from config.database import get_db
from config.logger import logger
from config.rules import get_current_user_permisions
from controllers.user import UserController
from models.user import UserSchema, UserCreateSchema

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    dependencies=[Depends(get_current_user_permisions)],
    responses={404: {"description": "Not found"}},
)


@router.get("/")
async def users(session: Session = Depends(get_db)) -> List[UserSchema]:
    """Get /users
    Args:
        session: Session
    Returns: list[UserSchema]
    """
    logger.info("GET /users - Listando usuarios")
    list_users = [
        UserSchema.from_orm(db_user)
        for db_user in UserController(session).get_all()
    ]
    return list_users


@router.get("/{user_id}")
async def read(user_id: str, session: Session = Depends(get_db)) -> UserSchema:
    """Get /users/{user_id}
    Args:
        user_id: id
        session: Session
    Returns: UserSchema
    """
    logger.info("GET /users/%s", user_id)
    db_user = UserController(session).get(int(user_id))
    if not db_user:
        logger.warning("GET /users usuario no encontrado id=%s", user_id)
        raise HTTPException(status_code=404, detail="User not Found")
    schema_user = UserSchema.from_orm(db_user)
    return schema_user


@router.put("/", response_model=UserSchema)
async def update(
    user: UserSchema, session: Session = Depends(get_db)
) -> UserSchema:
    """Put /users
    Args:
        user: UserSchema
        session: Session
    Returns: UserSchema
    """
    logger.info("PUT /users id=%s", user.id)
    controller = UserController(session)
    customer_db = controller.get(user.id)
    if not customer_db:
        logger.warning("PUT /users usuario no existe id=%s", user.id)
        raise HTTPException(status_code=404, detail="User not Found")
    return controller.update(user)


@router.post("/", response_model=UserSchema)
def create(
    user: UserCreateSchema, session: Session = Depends(get_db)
) -> UserSchema:
    """Post /users
    Args:
        user: UserCreateSchema
        session: Session
    Returns: UserSchema
    """
    logger.info("POST /users login=%s", user.login)
    controller = UserController(session)
    user_db = controller.get_by_login(user)
    if user_db:
        logger.warning("POST /users login ya registrado login=%s", user.login)
        raise HTTPException(status_code=400, detail="User already registered")
    new_user = controller.create(schema=user)
    if not new_user or not new_user.id:
        logger.warning("POST /users validación fallida login=%s", user.login)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Validation Error",
        )
    logger.info("POST /users creado id=%s", new_user.id)
    return UserSchema.from_orm(new_user)


@router.delete("/{user_id}")
def delete(user_id: str, session: Session = Depends(get_db)):
    """Delete /users/{user_id}
    Args:
        user_id: id
        session: Session
    Returns: result
    """
    logger.info("DELETE /users/%s", user_id)
    controller = UserController(session)
    user_db = controller.get(int(user_id))
    if not user_db:
        logger.warning("DELETE /users usuario no existe id=%s", user_id)
        raise HTTPException(status_code=404, detail="User not found")
    result = controller.delete(int(user_id))
    logger.info(
        "DELETE /users completado id=%s filas_afectadas=%s", user_id, result
    )
    return result

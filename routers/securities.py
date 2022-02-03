from fastapi import APIRouter
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from config.database import get_db
from config.hasher import get_access_token
from models.token import Token
from controllers.security import SecurityController

router = APIRouter(
    tags=["Security"],
    responses={404: {"description": "Not found"}},
)


@router.post("/token", response_model=Token)
async def login_for_access_token(
        session: Session = Depends(get_db),
        form_data: OAuth2PasswordRequestForm = Depends()):
    """ Post /token
    Args:
        session: Session
        form_data: OAuth2PasswordRequestForm

    Returns: dict
    {"access_token": access_token, "token_type": "bearer"}
    """
    controller = SecurityController(session)
    user = controller.authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await get_access_token(user)
    return {"access_token": access_token, "token_type": "bearer"}

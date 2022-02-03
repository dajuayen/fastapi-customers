from fastapi import Depends, status, HTTPException

from sqlalchemy.orm import Session

from config.database import get_db
from config.hasher import oauth2_scheme, get_user_from_token
from models.user import User


async def get_current_user(token: str = Depends(oauth2_scheme),
                           session: Session = Depends(get_db)):
    """Get current user

    Args:
        token: jwt-encoded access token
        session: Session

    Returns: User

    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        user = get_user_from_token(token, session)
        if user is None:
            raise credentials_exception
        return user
    except Exception as credential_error:
        raise credentials_exception from credential_error


async def get_current_active_user(
        current_user: User = Depends(get_current_user)):
    """  Check that the current user is active.
    Args:
        current_user: User
    Returns: boolean
    """
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


async def get_current_user_permisions(
        current_user: User = Depends(get_current_user)):
    """  Check that the current user has permission.
    Args:
        current_user: User
    Returns: boolean
    """
    if current_user.role == 'user':
        raise HTTPException(status_code=400,
                            detail="User has not permission")
    return current_user

from typing import Optional
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from jose import jwt
from models.token import TokenData
from models.user import User

SECRET_KEY = "989d770dbac3333a26ee0d897af4737c446b468ecda20f0d5c3c7d620d2493d9"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    """ It verifies that the plain text received is equal to the hashed
    password that is stored.

    Args:
        plain_password: password
        hashed_password: Password hashed and stored

    Returns: boolean
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    """Hashes the password that it receives as a parameter.

    Args:
        password: password (str)

    Returns: password hashed (str)
    """
    return pwd_context.hash(password)


def _create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """Create a jwt-encoded access token.

    Args:
        data: data to encode
        expires_delta: Time for the access token to expire.

    Returns: jwt-encoded access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_access_token(user):
    """ Return jwt-encoded access token

    Args:
        user: User

    Returns: jwt-encoded access token

    """
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    return _create_access_token(data={"sub": user.login},
                                expires_delta=access_token_expires)


def _get_user(login: str, session: Session):
    """ Search user by login and return it
    Args:
        login: str
        session: Session

    Returns: User or None
    """
    user = session.query(User).filter(User.login.like(login)).first()
    if user:
        return user
    return None


def get_user_from_token(token: str, session: Session):
    """ Return User from access token
    Args:
        token: str
        session: Session
    Returns: User
    """
    payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    token_data = TokenData(login=payload.get("sub"))
    user = _get_user(login=token_data.login, session=session)
    return user

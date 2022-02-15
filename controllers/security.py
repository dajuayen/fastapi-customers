from sqlalchemy.orm import Session

from config.hasher import verify_password
from controllers.user import UserController

from models.user import User


class SecurityController:
    """Security Controller"""

    def __init__(self, session=Session):
        self.session = session

    def authenticate_user(self, login: str, password: str) -> User:
        """ Authenticates the login and password in the system.
        Args:
            login: str
            password: str
        Returns: User or None
        """
        user = UserController(self.session).get_by_login(login=login)
        if not user:
            return False
        if not verify_password(password, user.hashed_password):
            return False
        return user

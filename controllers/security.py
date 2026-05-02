from sqlalchemy.orm import Session

from config.hasher import verify_password
from config.logger import logger
from controllers.user import UserController

from models.user import User


class SecurityController:
    """Security Controller"""

    def __init__(self, session=Session):
        self.session = session

    def authenticate_user(self, login: str, password: str) -> User:
        """Authenticates the login and password in the system.
        Args:
            login: str
            password: str
        Returns: User or None
        """
        user = UserController(self.session).get_by_login(login=login)
        if not user:
            logger.warning(
                "Autenticación fallida: usuario no encontrado login=%s", login
            )
            return False
        if not verify_password(password, user.hashed_password):
            logger.warning(
                "Autenticación fallida: contraseña incorrecta login=%s", login
            )
            return False
        logger.info("Autenticación correcta login=%s id=%s", login, user.id)
        return user

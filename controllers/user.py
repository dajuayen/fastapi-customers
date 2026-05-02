from sqlalchemy.orm import Session

from config.hasher import get_password_hash
from config.logger import logger
from controllers.controller import Controller
from models.user import User, UserSchema, UserCreateSchema, UserBaseSchema

ROLES = ["admin", "user"]

ADMIN_USER = {"login": "root", "password": "root", "role": "super"}


class UserController(Controller):
    """Customer Controller Class"""

    def __init__(self, session=Session, internal_class=User):
        super().__init__(session, internal_class)

    def get_by_login(self, user: UserBaseSchema = None, login: str = None):
        """Get user by login.
        Args:
            user: UserBaseSchema
            login: login (str)
        Returns: User
        """
        login = user.login if user else login
        return self.query.filter(User.login.like(login)).first()

    def _create_user(self, values):
        logger.info("Crear usuario login=%s", values.get("login"))
        db_user = User(**values)
        self.session.add(db_user)
        self.session.commit()
        self.session.refresh(db_user)
        logger.info("Usuario creado id=%s", db_user.id)
        return UserSchema.from_orm(db_user)

    def create_admin_user(self) -> UserSchema:
        """Create admin user
        Returns: Admin user or None
        """
        db_admin = self.get_by_login(login=ADMIN_USER.get("login"))
        if not db_admin:
            logger.info("Inicialización: creando usuario admin")
            vals = ADMIN_USER.copy()
            vals["hashed_password"] = get_password_hash(vals.pop("password"))
            return self._create_user(vals)
        logger.debug("Usuario admin ya existía")
        return False

    def create(self, schema: UserCreateSchema) -> UserSchema:
        """Create user.
        Args:
            schema: UserCreateSchema
        Returns: User or None
        """
        logger.info("UserController.create login=%s", schema.login)
        values = schema.dict()
        values["hashed_password"] = get_password_hash(values.pop("password"))
        if values.get("role") in ROLES:
            return self._create_user(values)
        logger.warning(
            "UserController.create rol no válido: %s", values.get("role")
        )
        return False

    def update(self, schema: UserSchema) -> UserSchema:
        """Update user.
        Args:
            schema: UserSchema
        Returns: User or None
        """
        return super().update(schema)

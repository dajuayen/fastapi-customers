from sqlalchemy.orm import Session

from controllers.controller import Controller
from controllers.security import get_password_hash
from models.user import User, UserSchema, UserCreateSchema

ROLES = ["admin", "user"]

ADMIN_USER = {
    "login": 'root',
    "password": 'root',
    "role": 'super'
}


class UserController(Controller):

    def __init__(self, session=Session, internal_class=User):
        self.db = session
        self.in_cls = internal_class
        self.q = self.db.query(self.in_cls)

    def get_by_login(self, user: UserCreateSchema = None, login: str = None):
        login = user.login if user else login
        return self.q.filter(User.login.like(login)).first()

    def _create_user(self, values):
        db_user = User(**values)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return UserSchema.from_orm(db_user)

    def create_admin_user(self) -> UserSchema:
        db_admin = self.get_by_login(login=ADMIN_USER.get('login'))
        if not db_admin:
            vals = ADMIN_USER.copy()
            vals['hashed_password'] = get_password_hash(vals.pop('password'))
            return self._create_user(vals)
        return False

    def create(self, user: UserCreateSchema) -> UserSchema:
        values = user.dict()
        values['hashed_password'] = get_password_hash(values.pop('password'))
        if values.get('role') in ROLES:
            return self._create_user(values)
        return False

    def update(self, user: UserSchema) -> UserSchema:
        return super(UserController, self).update(user)

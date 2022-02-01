from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.database import Base
from controllers.user import UserController

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                   bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        UserController(db).create_admin_user()
        yield db
    finally:
        db.close()

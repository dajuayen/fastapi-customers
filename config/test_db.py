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
    """ Generates test database connection session.
    Returns: Session
    """
    try:
        session = TestingSessionLocal()
        UserController(session).create_admin_user()
        yield session
    finally:
        session.close()

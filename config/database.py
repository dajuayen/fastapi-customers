from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.settings import settings

SQLALCHEMY_SQLITE_URL = f"sqlite:///{settings.path_base}/sql_app.db"
SQLALCHEMY_POSTGRES_URL = "postgresql://admin:admin@localhost:5432/customers_db"


def _get_url(env):
    if env == 'postgres':
        return SQLALCHEMY_POSTGRES_URL
    return SQLALCHEMY_SQLITE_URL


def _get_engine_attrs(env):
    if env == 'postgres':
        return {'pool_pre_ping': True}
    return {"connect_args": {
        "check_same_thread": False,
    }}


def get_engine(enviroment):
    """ Return engine of database
    Returns: engine
    """
    return create_engine(
        _get_url(enviroment),
        **_get_engine_attrs(enviroment)
    )


engine = get_engine(settings.env)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    """ Return session of connection to database
    Returns: Session
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()

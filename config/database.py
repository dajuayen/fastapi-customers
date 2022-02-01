from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from config.settings import Settings

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://admin:admin@postgresserver/db"

settings = Settings()


def _get_url(env):
    if env == 'test':
        return "sqlite:///./sql_app.db"
    elif env == 'postgres':
        return "postgresql://admin:admin@localhost:5432/customers_db"


def _get_engine_attrs(env):
    if env == 'test':
        return {"connect_args": {
            "check_same_thread": False,
        }}
    elif env == 'postgres':
        return {'pool_pre_ping': True}


def get_engine(settings):
    return create_engine(
        _get_url(settings.env),
        **_get_engine_attrs(settings.env)
    )


engine = get_engine(settings)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

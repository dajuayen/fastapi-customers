from typing import Generator

from sqlalchemy import create_engine
from sqlalchemy.dialects.postgresql import Any
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy_utils import database_exists, create_database, drop_database

import pytest
from fastapi.testclient import TestClient

from config.database import Base, get_db
from config.hasher import get_password_hash
from config.settings import settings
from main import app
from models.customer import Customer, CustomerSchema, CustomerCreateSchema
from models.user import User, UserSchema, UserCreateSchema

SQLALCHEMY_DATABASE_URL = f"sqlite:///{settings.path_base}/test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

users = [
    {
        'login': "root",
        'role': "root",
        'password': "root"},
    {
        'login': "admin",
        'role': "admin",
        'password': "admin"},
    {
        'login': "primero",
        'role': "user",
        'password': "1234"},
    {
        'login': "segundo",
        'role': "user",
        'password': "1234"},

]
customers = [
    {
        'name': "primero",
        'surname': "customer",
        'photo': "primero.png"},
    {
        'name': "segundo",
        'surname': "customer",
        'photo': "segundo.png"},
    {
        'name': "tercero",
        'surname': "customer",
        'photo': "tercero.png"}
]


def get_test_db():
    """Generate a test session.
    Returns: yield Session
    """
    # pylint: disable=C0103
    # SessionLocal = sessionmaker(bind=engine)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False,
                                bind=engine)
    test_db = SessionLocal()

    try:
        yield test_db
    finally:
        test_db.close()


def load_test_data(session):
    """Load data in test database"""
    for user_data in users:
        values = user_data.copy()
        values['hashed_password'] = get_password_hash(values.pop('password'))
        db_user = User(**values)
        session.add(db_user)
        session.commit()
        session.refresh(db_user)

    for customer_data in customers:
        db_customer = Customer(**customer_data)
        session.add(db_customer)
        session.commit()
        session.refresh(db_customer)


@pytest.fixture(scope="session", autouse=True)
def create_test_database():
    """
    Create a clean database on every test case.
    We use the `sqlalchemy_utils` package here for a few helpers in consistently
    creating and dropping the database.
    """
    # pylint: disable=C0103
    if not database_exists(SQLALCHEMY_DATABASE_URL):
        # drop_database(SQLALCHEMY_DATABASE_URL)
        create_database(SQLALCHEMY_DATABASE_URL)  # Create the test database.
        Base.metadata.create_all(engine)  # Create the tables.
        app.dependency_overrides[
            get_db] = get_test_db  # Mock the Database Dependency
        Session_Local = sessionmaker(autocommit=False, autoflush=False,
                                     bind=engine)
        session = Session_Local()
        load_test_data(session)

    yield  # Run the tests.
    drop_database(SQLALCHEMY_DATABASE_URL)  # Drop the test database.


@pytest.fixture
def test_db_session():
    """Returns an sqlalchemy session, and after the test tears down everything
    properly.
    """
    # pylint: disable=C0103
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session: Session = SessionLocal()
    yield session
    # Drop all data after each test
    # for tbl in reversed(Base.metadata.sorted_tables):
    #     engine.execute(tbl.delete())
    # put back the connection to the connection pool
    session.close()


@pytest.fixture
def test_db_session_clean():
    """Returns an sqlalchemy session, and after the test tears down everything
    properly.
    """
    # pylint: disable=C0103
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session: Session = SessionLocal()
    yield session
    # Drop all data after each test
    for tbl in reversed(Base.metadata.sorted_tables):
        engine.execute(tbl.delete())
    # put back the connection to the connection pool
    session.close()


@pytest.fixture(name="client")
def fixture_client() -> Generator[TestClient, Any, None]:
    """Return a TestClient"""
    with TestClient(app) as new_client:
        yield new_client


@pytest.fixture
def admin():
    """Return a UserSchema with admin user's data"""
    return UserSchema(login="admin", role="admin", id=2)


@pytest.fixture
def user():
    """Return a UserSchema with a user's data"""
    return UserSchema(login="primero", role="user", id=3)


@pytest.fixture
def new_user():
    """Return a UserCreateSchema with a new user's data"""
    return UserCreateSchema(login="nuevo", role="user", password="1234")


@pytest.fixture
def customer1():
    """Return a CustomerSchema with customer1's data"""
    return CustomerSchema(name="primero", surname="customer",
                          photo="primero.png", id=1)


@pytest.fixture
def customer3():
    """Return a CustomerSchema with customer2's data"""
    return CustomerSchema(name="tercero", surname="customer",
                          photo="tercero.png", id=3)


@pytest.fixture
def new_customer():
    """Return a CustomerCreateSchema with a new customer's data"""
    return CustomerCreateSchema(name="nuevo", surname="customer",
                          photo="nuevo.png")


@pytest.fixture
def login_admin(client):
    """Return Authorization from admin user's login"""
    login_data = {
        "username": "admin",
        "password": "admin"
    }
    response = client.post("/token", data=login_data)
    data = response.json()
    auth = f'{data.get("token_type")} {data.get("access_token")}'
    return {"Authorization": auth}


@pytest.fixture
def login_user(client):
    """Return Authorization from a user's login"""
    login_data = {
        "username": "primero",
        "password": "1234"
    }
    response = client.post("/token", data=login_data)
    data = response.json()
    auth = f'{data.get("token_type")} {data.get("access_token")}'
    return {"Authorization": auth}

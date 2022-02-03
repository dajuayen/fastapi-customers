"""Test Module. Main endpoint"""
from fastapi.testclient import TestClient

from config.database import get_db, Base
from config.test_db import override_get_db, engine
from main import app

Base.metadata.create_all(bind=engine)

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_read_main():
    """Test main endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.request.path_url == "/docs"

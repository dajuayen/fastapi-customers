import pytest

from test.test_main import client


@pytest.fixture
def fixtures_OAuth2PasswordRequestForm():
    return


def test_login_for_access_token():

    login_data = {
        "username": "root",
        "password": "root"
    }
    r = client.post("/token", data=login_data)
    # response = client.post("/webrecord/check_if_object_exist/key",
    #                       params={"data": "my_data"}) ¿funcionará?
    # response = client.post("/token",
    #                        data={"username": "loli", "password": "1234",
    #                              "grant_type": "password"},
    #                        headers={
    #                            "content-type": "application/x-www-form-urlencoded"})
    # response = client.post("/token",
    #                       params={"username": "admin", "password": "admin"})
    assert r.status_code == 200
    response_data = r.json()
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"
    return response_data["token_type"], response_data["access_token"]

from test.test_main import client

# import pytest
#
#
# @pytest.fixture
# def fixtures_OAuth2PasswordRequestForm():
#     """
#
#     Returns:
#
#     """
#     return


def test_login_for_access_token():
    """Check that an access_token is returned when logging in and
    that it is of type bearer.
    """
    login_data = {
        "username": "root",
        "password": "root"
    }
    response = client.post("/token", data=login_data)
    # response = client.post(
    #     "/token", data=login_data,
    #     headers={"content-type": "application/x-www-form-urlencoded"})
    assert response.status_code == 200
    response_data = response.json()
    assert "access_token" in response_data
    assert response_data["token_type"] == "bearer"

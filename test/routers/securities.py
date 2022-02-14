# pylint: disable=R0201


class TestTokenRouter:
    """Test Tocken Router"""

    def test_login_root(self, client):
        """Check that an access_token is returned when logging in and
        that it is of type bearer.
        """
        login_data = {
            "username": "root",
            "password": "root"
        }
        response = client.post("/token", data=login_data)
        assert response.status_code == 200
        response_data = response.json()
        assert "access_token" in response_data
        assert response_data["token_type"] == "bearer"

    def test_login_admin(self, client):
        """Check that an access_token is returned when logging in and
        that it is of type bearer.
        """
        login_data = {
            "username": "admin",
            "password": "admin"
        }
        response = client.post("/token", data=login_data)
        assert response.status_code == 200
        response_data = response.json()
        assert "access_token" in response_data
        assert response_data["token_type"] == "bearer"

    def test_login_user(self, client):
        """Check that an access_token is returned when logging in and
        that it is of type bearer.
        """
        login_data = {
            "username": "primero",
            "password": "1234"
        }
        response = client.post("/token", data=login_data)
        assert response.status_code == 200
        response_data = response.json()
        assert "access_token" in response_data
        assert response_data["token_type"] == "bearer"

    def test_login_password_fail(self, client):
        """Check that 401 status code was returned when the password was wrong.
        """
        login_data = {
            "username": "root",
            "password": "1234"
        }
        response = client.post("/token", data=login_data)
        assert response.status_code == 401

    def test_login_non_user(self, client):
        """Check that 401 status code was returned when the user doesn't exist.
        """
        login_data = {
            "username": "no_user",
            "password": "root"
        }
        response = client.post("/token", data=login_data)
        assert response.status_code == 401

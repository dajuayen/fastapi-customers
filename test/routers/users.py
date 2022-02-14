from models.user import UserSchema


class TestUsersRouter:
    """Test Users Router"""
    # pylint: disable=R0201

    def test_users(self, admin, client, login_admin):
        """Check that an access_token is returned when logging in and
        that it is of type bearer.
        """
        response = client.get("/users",
                              headers=login_admin)
        assert response.status_code == 200
        users = response.json()
        assert admin in users

    def test_get_admin(self, admin, client, login_admin):
        """ Find a admin user.
        Args:
            admin: schema
            client: testClient
            login_admin: authorization
        """
        url = f"/users/{admin.id:d}"
        response = client.get(url=url, headers=login_admin)
        assert response.status_code == 200
        response_user = response.json()
        assert admin == UserSchema(**response_user)

    def test_get_user(self, user, client, login_admin):
        """ Find a user.
        Args:
            user: schema
            client: testClient
            login_admin: authorization
        """
        url = f"/users/{user.id:d}"
        response = client.get(url=url, headers=login_admin)
        assert response.status_code == 200
        response_user = response.json()
        assert user == UserSchema(**response_user)

    def test_create_delete_user(self, new_user, client, login_admin):
        """ Check to create a user. After check to delete the created user.
        Args:
            new_user: schema
            client: testClient
            login_admin: authorization
        """
        values = new_user.dict()
        response = client.post("/users/", headers=login_admin, json=values)
        assert response.status_code == 200
        response_user = response.json()
        create_user = UserSchema(**response_user)
        assert new_user.login == create_user.login

        url = f"/users/{create_user.id:d}"
        response = client.delete(url, headers=login_admin)
        assert response.status_code == 200

    def test_update_user(self, user, client, login_admin):
        """ Check to update a user.
        Args:
            user: schema
            client: testClient
            login_admin: authorization
        """
        values = user.dict()
        values['login'] = "primer"
        values['role'] = "admin"
        response = client.put("/users/", headers=login_admin, json=values)
        assert response.status_code == 200
        response_user = response.json()
        modified_user = UserSchema(**response_user)
        assert user.id == modified_user.id
        assert user.login != modified_user.login
        assert modified_user.login == "primer"
        assert user.role != modified_user.role
        assert modified_user.role == "admin"

        values['login'] = "primero"
        values['role'] = "user"
        response = client.put("/users/", headers=login_admin, json=values)
        assert response.status_code == 200
        response_user = response.json()
        restored_user = UserSchema(**response_user)
        assert restored_user.id == modified_user.id
        assert user.id == restored_user.id

        assert restored_user.login != modified_user.login
        assert user.login == restored_user.login
        assert restored_user.login == "primero"

        assert restored_user.role != modified_user.role
        assert user.role == restored_user.role
        assert restored_user.role == "user"

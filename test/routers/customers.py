# pylint: disable=unused-import
from test.conftest import customer1, customer3


import pytest

from models.customer import CustomerSchema


class TestCustomersRouter:
    """Test Customers Router"""
    # pylint: disable=R0201

    def test_customers_wo_login(self, client):
        """Check that without being logged in you cannot access /customers.
        """
        response = client.get("/customers")
        assert response.status_code == 401

    def test_customers_login_admin(self, customer1, client, login_admin):
        """Check that you can access the list of customers as an admin user.
        """
        # pylint: disable=redefined-outer-name
        response = client.get("/customers", headers=login_admin)
        assert response.status_code == 200
        customers = response.json()
        assert customer1 in customers

    def test_customers_login_user(self, customer1, client, login_user):
        """Check that you can access the list of customers as a basic user.
        """
        # pylint: disable=redefined-outer-name
        response = client.get("/customers", headers=login_user)
        assert response.status_code == 200
        customers = response.json()
        assert customer1 in customers

    @pytest.mark.parametrize("customer_fixture", ['customer1', 'customer3'])
    def test_get_customer_wo_login(
            self, customer_fixture, client, request):
        """Check that you have to be logged in to retrieve a customer's data.
        """
        customer_schema = request.getfixturevalue(customer_fixture)
        url = f"/customers/{customer_schema.id:d}"
        response = client.get(url=url)
        assert response.status_code == 401

    @pytest.mark.parametrize("customer_fixture, login_fixture",
                             [('customer1', 'login_admin'),
                              ('customer1', 'login_user'),
                              ('customer3', 'login_admin'),
                              ('customer3', 'login_user')])
    def test_get_customer_login(
            self, customer_fixture, client, login_fixture, request):
        """Check that it returns data from a customer if the user, be it a
        basic user or admin, is logged in.
        """
        customer_schema = request.getfixturevalue(customer_fixture)
        login = request.getfixturevalue(login_fixture)
        url = f"/customers/{customer_schema.id:d}"
        response = client.get(url=url, headers=login)
        assert response.status_code == 200
        result = response.json()
        assert customer_schema == result

    @pytest.mark.parametrize("customer_fixture, login_fixture",
                             [('customer1', 'login_admin'),
                              ('customer1', 'login_user'),
                              ('customer3', 'login_admin'),
                              ('customer3', 'login_user')])
    def test_update_customer(self, customer_fixture, client, login_fixture,
                             request):
        """ Check to update a user.
        Args:
            customer: schema
            client: testClient
            login_admin: authorization
        """
        customer = request.getfixturevalue(customer_fixture)
        login = request.getfixturevalue(login_fixture)
        values = customer.dict()
        values['name'] = customer.name + "modified"
        values['surname'] = customer.name + "modified"
        response = client.put("/customers/", headers=login, json=values)
        assert response.status_code == 200
        response_customer = response.json()
        modified_customer = CustomerSchema(**response_customer)
        assert customer.id == modified_customer.id
        assert customer.name != modified_customer.name
        assert customer.surname != modified_customer.surname
        assert "modified" in modified_customer.name
        assert "modified" in modified_customer.surname

        values['name'] = customer.name
        values['surname'] = customer.surname
        response = client.put("/customers/", headers=login, json=values)
        assert response.status_code == 200
        response_customer = response.json()
        restored_customer = CustomerSchema(**response_customer)
        assert restored_customer.id == modified_customer.id
        assert customer.id == restored_customer.id

        assert restored_customer.name != modified_customer.name
        assert customer.name == restored_customer.name
        assert restored_customer.name == customer.name

        assert restored_customer.surname != modified_customer.surname
        assert customer.surname == restored_customer.surname
        assert restored_customer.surname == customer.surname

    @pytest.mark.parametrize("customer_fixture", ['customer1', 'customer3'])
    def test_update_customer_wo_login(self, customer_fixture, client, request):
        """ Check to update a user without logging it's not posible.
        Args:
            customer: schema
            client: testClient
            login_admin: authorization
        """
        customer = request.getfixturevalue(customer_fixture)
        values = customer.dict()
        values['name'] = customer.name + "modified"
        values['surname'] = customer.name + "modified"
        response = client.put("/customers/", json=values)
        assert response.status_code == 401

    @pytest.mark.parametrize("login_fixture", ['login_admin', 'login_user'])
    def test_create_delete_customer(self, new_customer, client, login_fixture,
                                    request):
        """ Check to create a user. After check to delete the created user.
        Args:
            new_user: schema
            client: testClient
            login_admin: authorization
        """
        values = new_customer.dict()
        login = request.getfixturevalue(login_fixture)
        response = client.post("/customers/", headers=login, json=values)
        assert response.status_code == 200
        response_customer = response.json()
        create_customer = CustomerSchema(**response_customer)
        assert new_customer.name == create_customer.name
        assert new_customer.surname == create_customer.surname
        assert new_customer.photo == create_customer.photo

        url = f"/customers/{create_customer.id:d}"
        response = client.delete(url, headers=login)
        assert response.status_code == 200

from controllers.customer import CustomerController
from models.customer import CustomerBaseSchema


class TestCustomerController:
    """Test CustomerController"""
    # pylint: disable=R0201

    def test_get_by_name_surname(self, test_db_session):
        """Find customer by name and surname.
        Args:
            test_db_session: Session
        """
        controller = CustomerController(test_db_session)
        customer = CustomerBaseSchema(name="primero", surname="customer")
        db_customer = controller.get_by_name_surname(customer)
        result_customer = CustomerBaseSchema.from_orm(db_customer)
        assert customer == result_customer


# class CustomerControllerTest(unittest.TestCase):
#
#     @classmethod
#     def setUp(cls):
#         cls.session = get_test_db()
#         for customer in CustomerControllerTest.get_customers():
#             pprint(customer)
#             CustomerControllerTest.create_customer(customer)
#
#     @classmethod
#     def create_customer(cls, customer):
#         cls.session.add(customer)
#         cls.session.commit()
#         cls.session.refresh(customer)
#         return customer
#
#     @classmethod
#     def get_customers(cls):
#         maria = Customer(**{
#             "name": "María",
#             "surname": "DelaO",
#             "photo": "maria.png"
#         })
#         elena = Customer(**{
#             "name": "Elena",
#             "surname": "García",
#             "photo": "elena.png"
#         })
#         return [maria, elena]
#
#     def test_get_by_name_surname(self):
#         controller = CustomerController(self.session)
#         customer = CustomerBaseSchema(name="Elena", surname="García")
#         db_customer = controller.get_by_name_surname(customer)
#         result_customer = CustomerBaseSchema.from_orm(db_customer)
#         self.assertEqual(customer, result_customer,
#                          'wrong result')

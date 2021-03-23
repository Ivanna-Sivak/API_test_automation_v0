from models.user import UserModel
from tests.unit.unit_base_test import UnitBaseTest


class UserTest(UnitBaseTest):
    def test_create_user(self):
        user = UserModel('test_name', 'test_password')
        self.assertEqual(user.username, 'test_name')
        self.assertEqual(user.password, 'test_password')
        
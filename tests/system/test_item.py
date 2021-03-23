from models.item import ItemModel
from models.store import StoreModel
from models.user import UserModel
from tests.base_test import BaseTest
import json


class ItemTest(BaseTest):
    def setUp(self):
        super(ItemTest, self).setUp()
        with self.app() as client:
            with self.app_context():
                UserModel('test', '1234').save_to_db()
                auth_request = client.post('/auth', data=json.dumps(
                    {'username': 'test', 'password': '1234'}),
                                           headers={'Content-Type': 'application/json'})
                auth_token = json.loads(auth_request.data)['access_token']
                self.access_token = f'JWT {auth_token}'

    def test_get_item_no_auth(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/item/test')
                self.assertEqual(response.status_code, 401)

    def test_get_item_not_found(self):
        with self.app() as client:
            with self.app_context():
                header = {'Authorization': self.access_token}
                response = client.get('/item/test', headers=header)

                self.assertEqual(response.status_code, 404)
                self.assertDictEqual(json.loads(response.data), {'message': 'Item not found'})

    def test_get_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 10, 1).save_to_db()
                header = {'Authorization': self.access_token}
                response = client.get('/item/test', headers=header)

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), {'name': 'test', 'price': 10.0})

    def test_delete_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                ItemModel('test', 10, 1).save_to_db()
                response = client.delete('/item/test')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), {'message': 'Item deleted'})

    def test_create_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.post('/item/test', data={'price': 10, 'store_id': 1})

                self.assertEqual(response.status_code, 201)
                self.assertDictEqual(json.loads(response.data), {'name': 'test', 'price': 10.0})

    def test_create_duplicate_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                client.post('/item/test', data={'price': 10, 'store_id': 1})
                response = client.post('/item/test', data={'price': 10, 'store_id': 1})

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(json.loads(response.data),
                                     {'message': "An item with name 'test' already exists."})

    def test_put_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                response = client.put('/item/test', data={'price': 10, 'store_id': 1})

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), {'name': 'test', 'price': 10.0})

    def test_put_update_item(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                client.post('/item/test', data={'price': 10, 'store_id': 1})
                response = client.put('/item/test', data={'price': 9.99, 'store_id': 1})
                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), {'name': 'test', 'price': 9.99})

    def test_item_list(self):
        with self.app() as client:
            with self.app_context():
                StoreModel('test').save_to_db()
                client.post('/item/test', data={'price': 10, 'store_id': 1})
                response = client.get('/items')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data),
                                     {'items': [{'name': 'test', 'price': 10.0}]})


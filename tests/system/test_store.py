from models.store import StoreModel
from models.item import ItemModel
from tests.base_test import BaseTest
import json


class StoreTest(BaseTest):
    def test_create_store(self):
        with self.app() as client:
            with self.app_context():
                response = client.post('/store/test', data=json.dumps({'name': 'test'}))

                self.assertEqual(response.status_code, 201)
                self.assertIsNotNone(StoreModel.find_by_name('test'))
                self.assertDictEqual(json.loads(response.data),
                                     {'id': 1, 'name': 'test', 'items': []})

    def test_create_duplicate_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test', data=json.dumps({'name': 'test'}))
                response = client.post('/store/test', data=json.dumps({'name': 'test'}))

                self.assertEqual(response.status_code, 400)
                self.assertDictEqual(json.loads(response.data),
                                     {'message': "A store with name 'test' already exists."})

    def test_delete_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test', data=json.dumps({'name': 'test'}))
                response = client.delete('/store/test', data=json.dumps({'name': 'test'}))

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data), {'message': 'Store deleted'})
                self.assertIsNone(StoreModel.find_by_name('test'))

    def test_find_store(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test', data=json.dumps({'name': 'test'}))
                response = client.get('/store/test')

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data),
                                     {'id': 1, 'name': 'test', 'items': []})

    def test_store_not_found(self):
        with self.app() as client:
            with self.app_context():
                response = client.get('/store/test', data=json.dumps({'name': 'test'}))

                self.assertEqual(response.status_code, 404)
                self.assertDictEqual(json.loads(response.data), {'message': 'Store not found'})

    def test_store_found_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test', data=json.dumps({'name': 'test'}))
                ItemModel('test_item', 10, 1).save_to_db()
                response = client.get('/store/test', data=json.dumps({'name': 'test'}))

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data),
                {'id': 1, 'name': 'test', 'items': [{'name': 'test_item', 'price': 10.0}]})

    def store_list(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test', data=json.dumps({'name': 'test'}))
                response = client.get('/stores', data=json.dumps({'name': 'test'}))

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data),
                                     {'stores': [{'name': 'test', 'items': []}]})

    def store_list_with_items(self):
        with self.app() as client:
            with self.app_context():
                client.post('/store/test', data=json.dumps({'name': 'test'}))
                ItemModel('test_item', 10, 1).save_to_db()
                response = client.get('/stores', data=json.dumps({'name': 'test'}))

                self.assertEqual(response.status_code, 200)
                self.assertDictEqual(json.loads(response.data),
                                     {'stores': [{'name': 'test_item', 'price': 10.0}]})



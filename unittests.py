import sys
import unittest
from controller import app

class ServerTests(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
    def test_hello_world(self):
        def should_receive_success():
            response = self.tester.get('/', content_type='html/text')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.data, b'Hello, World!')

        should_receive_success()
        
    def test_get(self):
        self.assertEqual(200, 200)


class MerchantTests(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
    def test_get(self):
        pass
    def test_post(self):
        pass
    def test_put(self):
        pass
    def test_patch(self):
        pass
    def test_delete(self):
        pass


class InvoiceTests(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
        self.mock_json = {
            "name": "Nikhil",
            "token": "12345678900000000000000000000000",
            "amount": "10",
            "items": [
                {
                    "name": "taco",
                    "price": "10",
                    "quantity": "1"
                }
            ]
        }


    def test_get(self):
        def should_get_correct_invoice():
            response = self.tester.get('/invoices/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'1':self.mock_json})

        should_get_correct_invoice()


    def test_post(self):
        json = {
            "name": "Nikhil",
            "token": "12345678900000000000000000000000",
            "amount": "10",
            "items": [
                {
                    "name": "taco",
                    "price": "10",
                    "quantity": "1"
                }
            ]
        }

        def should_receive_success():
            response = self.tester.post('/invoices', json=json)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'success')

        should_receive_success()

    def test_put(self):
        pass

    def test_patch(self):
        json = {'name':'Kyle'}

        def should_receive_success():
            response = self.tester.patch('/invoices/1', json=json)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'success')
            self.assertEqual(response.json['id'], '1')

        def should_change_name():
            patch_mock_json = self.mock_json
            patch_mock_json['name'] = 'Kyle'
            response = self.tester.get('/invoices/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json, {'1':self.mock_json})

        should_receive_success()
        should_change_name()

    def test_delete(self):
        def should_receive_success():
            response = self.tester.delete('/invoices/2')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'success')
            self.assertEqual(response.json['id'], '2')

        def should_no_longer_exist():
            response = self.tester.get('/invoices/2')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'fail')
            self.assertEqual(response.json['id'], '2')

        should_receive_success()
        should_no_longer_exist()

        
if __name__ == '__main__':
    test_classes_to_run = [ServerTests, InvoiceTests, MerchantTests]
    loader = unittest.TestLoader()

    suites_list = []
    for test_class in test_classes_to_run:
        suite = loader.loadTestsFromTestCase(test_class)
        suites_list.append(suite)

    big_suite = unittest.TestSuite(suites_list)

    runner = unittest.TextTestRunner()
    results = runner.run(big_suite)
    '''

    suite = unittest.TestLoader().loadTestsFromModule( sys.modules[__name__] )
    unittest.TextTestRunner(verbosity=3).run( suite )
    '''


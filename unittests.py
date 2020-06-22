''' unittests.py
'''
import sys
import json
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
    def test_visa_api(self):
        def should_receive_success():
            response = self.tester.get('/visa-api-test')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(json.loads(response.data.decode('utf-8'))['message'],'helloworld')
        should_receive_success()
        
    def test_get(self):
        self.assertEqual(200, 200)


class MerchantTests(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)

    def test_get(self):
        response = self.tester.get('/merchants/1')
        self.assertEqual(response.status_code, 200)

    def test_post(self):
        response = self.tester.post('/merchants',json={})
        self.assertEqual(response.status_code, 200)

    def test_put(self):
        response = self.tester.put('/merchants',json={})
        self.assertEqual(response.status_code, 200)

    def test_patch(self):
        response = self.tester.patch('/merchants',json={})
        self.assertEqual(response.status_code, 200)

    def test_delete(self):
        response = self.tester.delete('/merchants',json={})
        self.assertEqual(response.status_code, 200)


class InvoiceTests(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
        self.mock_json_order_info = {
            "invoiceAmt": "10",
            "invoiceDesc": "1 taco for 10 dollars"
        }
        self.mock_json_with_account = dict(
            {"merchantid": "12345678900000000000000000000000"},
            **self.mock_json_order_info
        )
        self.mock_json_no_account = dict({
            "bin": "123456",
            "pan": "12345678900000000000000000000000",
            "name": "Kyle",
            "country": "us"},
            **self.mock_json_order_info
        )


    def test_get(self):
        def should_get_correct_invoice_with_account():
            response = self.tester.get('/invoices/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], {'1':self.mock_json_with_account})

        should_get_correct_invoice_with_account()


    def test_post(self):
        def should_receive_success():
            response = self.tester.post('/invoices', json=self.mock_json_with_account)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'success')
        def should_receive_success_no_account():
            response = self.tester.post('/invoices', json=self.mock_json_no_account)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'success')
        '''
        def should_fail_if_invalid_record():
            self.mock_json['invalidfield'] = 'foobar'
            response = self.tester.post('/invoices', json=self.mock_json_no_account)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'fail')
        '''

        should_receive_success()
        should_receive_success_no_account()
        #should_fail_if_invalid_record()

    def test_put(self):
        put_mock_json = dict(**self.mock_json_no_account)
        put_mock_json['invoiceAmt'] = '99'

        def should_receive_success():
            response = self.tester.put('/invoices/1', json=put_mock_json)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'success')
            self.assertEqual(response.json['id'], '1')

        def should_change_record():
            response = self.tester.get('/invoices/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], {'1':put_mock_json})

        should_receive_success()
        should_change_record()

    def test_patch(self):
        json = {'invoiceAmt':'20'}

        def should_receive_success():
            response = self.tester.patch('/invoices/1', json=json)
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['status'], 'success')
            self.assertEqual(response.json['id'], '1')

        def should_change_record():
            patch_mock_json = dict(**self.mock_json_with_account)
            patch_mock_json['invoiceAmt'] = '20'
            response = self.tester.get('/invoices/1')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], {'1':patch_mock_json})

        should_receive_success()
        should_change_record()

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


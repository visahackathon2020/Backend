''' unittests.py
'''
import sys
import json
import unittest
from controller import app

from tests import MerchantTests as M
from tests import InvoiceTests as I

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


if __name__ == '__main__':
    test_classes_to_run = [ServerTests, I.InvoiceTests, M.MerchantTests]
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

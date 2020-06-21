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
        
if __name__ == '__main__':
    unittest.main()

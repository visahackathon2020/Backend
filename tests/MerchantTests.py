''' merchanttests.py
'''
import sys
import json
import unittest
from server import app

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


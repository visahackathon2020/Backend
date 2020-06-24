''' invoicetests.py
'''
import sys
import json
import unittest
from server import app

class VisaFundsPushTests(unittest.TestCase):
    def setUp(self):
        self.tester = app.test_client(self)
        self.test_data = {
            "senderAccountNumber": "495703042020470",
            "recipientPrimaryAccountNumber": "4957030420210454",
            "cardAcceptor.name": "Acceptor 2",
            "cardAcceptor.address.country": "CAN",
            "cardAcceptor.address.state": "AB",
            "transactionCurrencyCode": "CAD",
            "amount": "200",
            "acquiringBin": "408999"
        }

    def test_data(self):
        response = self.tester.post(f'/visa-push-test', json=self.test_data)
        print(response.content)
        self.assertEqual(response.status_code, 200)


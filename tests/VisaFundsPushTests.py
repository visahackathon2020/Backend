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
            "acquirerCountryCode": "840",
            "acquiringBin": "408999",
            "amount": "124.05",
            "businessApplicationId": "AA",
            "cardAcceptor": {
                "address": {
                    "country": "USA",
                    "county": "San Mateo",
                    "state": "CA",
                    "zipCode": "94404"
                    },
                "idCode": "CA-IDCode-77765",
                "name": "Visa Inc. USA-Foster City",
                "terminalId": "TID-9999"
                },
            "localTransactionDateTime": "2020-06-24T16:08:34",
            "merchantCategoryCode": "6012",
            "pointOfServiceData": {
                "motoECIIndicator": "0",
                "panEntryMode": "90",
                "posConditionCode": "00"
                },
            "recipientName": "rohan",
            "recipientPrimaryAccountNumber": "4957030420210496",
            "retrievalReferenceNumber": "412770451018",
            "senderAccountNumber": "4653459515756154",
            "senderAddress": "901 Metro Center Blvd",
            "senderCity": "Foster City",
            "senderCountryCode": "124",
            "senderName": "Mohammed Qasim",
            "senderReference": "",
            "senderStateCode": "CA",
            "sourceOfFundsCode": "05",
            "systemsTraceAuditNumber": "451018",
            "transactionCurrencyCode": "USD",
            "transactionIdentifier": "381228649430015",
            "settlementServiceIndicator": "9",
            "colombiaNationalServiceData": {
                "countryCodeNationalService": "170",
                "nationalReimbursementFee": "20.00",
                "nationalNetMiscAmountType": "A",
                "nationalNetReimbursementFeeBaseAmount": "20.00",
                "nationalNetMiscAmount": "10.00",
                "addValueTaxReturn": "10.00",
                "taxAmountConsumption": "10.00",
                "addValueTaxAmount": "10.00",
                "costTransactionIndicator": "0",
                "emvTransactionIndicator": "1",
                "nationalChargebackReason": "11"
            }
        }
        self.bad_test_data = {
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
        print(json.dumps(response.data))
        self.assertEqual(response.status_code, 200)


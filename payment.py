from helpers import decorate_all_methods, return_status
from visa_api import visa_api_call
from flask import request
from flask_restful import Resource
from db import PaymentSchema

from db import database
from datetime import datetime
import requests

# Testing visa API calls
def visa_push_funds(json):
    url = 'https://sandbox.api.visa.com/visadirect/fundstransfer/v1/pushfundstransactions'
    headers = {"Content-Type":"application/json", "Accept":"application/json"}
    x = visa_api_call(url, methodType=requests.post, headers=headers, json=json).json()
    return x

@decorate_all_methods(return_status)
class Payment(Resource):
    def post(self):
        # verify JSON with schema
        sender_json = PaymentSchema().load(request.json)

        # Get the invoices obj from the given code
        code = sender_json['invoiceId']
        doc_ref = database.collection(u'invoices').document(code)
        doc = doc_ref.get()
        if not doc.exists:
            return {'status':'fail', 'result':'Record doesn\'t exist with given invoiceId'}
        invoice = doc.to_dict()

        # Get the date and audit number
        now = datetime.now()
        auditNumber = str(hash(sender_json['invoiceId']) % 1000000).zfill(6)
        retrievalReferenceNumber = now.strftime("%y")[1] + now.strftime("%j%H") + auditNumber
        #retrievalReferenceNumber = retrievalReferenceNumber + retrievalReferenceNumber

        # Build the json to send
        json = {
            "amount": str(sum([float(item['amount']) for item in invoice['items']])),
            "recipientPrimaryAccountNumber": invoice['PAN'],
            'senderAccountNumber': sender_json['senderPAN'],
            "localTransactionDateTime": now.strftime('%Y-%m-%dT%H:%M:%S'),
            "retrievalReferenceNumber": retrievalReferenceNumber,
            "systemsTraceAuditNumber": auditNumber,
            "acquirerCountryCode": "840",
            "acquiringBin": "408999",
            "businessApplicationId": "AA",
            "cardAcceptor": {
            "address": {
            "country": "USA",
            "state": "CA",
            "zipCode": "94404"
            },
            "idCode": "CA-IDCode-77765",
            "name": "Visa Inc. USA-Foster City",
            "terminalId": "TID-9999"
            },
            "transactionCurrencyCode": "USD"

        }

        # TODO delete the invoice if confirmed successful funds transaction

        return visa_push_funds(json)


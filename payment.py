from helpers import decorate_all_methods, return_status
from visa_api import visa_api_call
from flask import request
from flask_restful import Resource
from db import PaymentSchema

from db import database
from datetime import datetime
import requests
import json
import os

# Testing visa API calls
def visa_push_funds(json):
    url = 'https://sandbox.api.visa.com/visadirect/fundstransfer/v1/pushfundstransactions'
    headers = {"Content-Type":"application/json", "Accept":"application/json"}
    x = visa_api_call(url, methodType=requests.post, headers=headers, json=json)
    return x

def visa_pull_funds(json):
    url = 'https://sandbox.api.visa.com/visadirect/fundstransfer/v1/pullfundstransactions'
    headers = {"Content-Type":"application/json", "Accept":"application/json"}
    x = visa_api_call(url, methodType=requests.post, headers=headers, json=json)
    return x

@decorate_all_methods(return_status)
class Payment(Resource):
    def post(self):
        # verify JSON with schema
        load_json = request.json
        if load_json is None:
            load_json = json.loads(request.data)
        sender_json = PaymentSchema().load(load_json)

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
        # Build the push json to send
        api_json = {
            "amount": str(sum([float(item['amount']) for item in invoice['items']])),
            "recipientPrimaryAccountNumber": invoice['PAN'],
            "localTransactionDateTime": now.strftime('%Y-%m-%dT%H:%M:%S'),
            "retrievalReferenceNumber": retrievalReferenceNumber,
            "systemsTraceAuditNumber": auditNumber,
            "acquirerCountryCode": "840",
            "acquiringBin": os.getenv("acquiringBin"),
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
            }

        }

        pull_api_json = dict({
            'senderPrimaryAccountNumber': sender_json['senderPAN'],
            "acquirerCountryCode": "840",
            "senderCurrencyCode":"USD",
            "senderCardExpiryDate": "2015-10",
            "cpsAuthorizationCharacteristicsIndicator": "Y"
        }, **api_json)


        push_api_json = dict({
            'senderAccountNumber': sender_json['senderPAN'],
            "transactionCurrencyCode": "USD"
        }, **api_json)


        # Build the pull json to send
        pull_res = visa_pull_funds(pull_api_json)
        assert pull_res.status_code == 200, "Pull:" + str(pull_res.content)

        push_res = visa_push_funds(push_api_json)
        assert push_res.status_code == 200, "Push:" + str(push_res.content)
       
        return push_res.json()


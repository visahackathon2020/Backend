#!flask/bin/python
''' server.py
Description of the purpose of this file
'''
from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS, cross_origin
import requests
import os
import sys
from dotenv import load_dotenv
import json
from datetime import datetime
from db import invoices
from db import database


load_dotenv() # Load environment variables
certs_dir_path = os.path.dirname(os.path.realpath(__file__)) + '/certs' # path to our certs

app = Flask(__name__)
api = Api()
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Methods'] = '*'
    header['Access-Control-Allow-Headers'] = '*'
    header['Access-Control-Allow-Origin'] = '*'
    return response

from invoices import Invoice
from merchants import Merchant
api.add_resource(Invoice,'/invoices','/invoices/', '/invoices/<string:id>')
api.add_resource(Merchant,'/merchants', '/merchants/<string:id>')
api.init_app(app)

# Testing Flask
@app.route('/')
def index():
    return "Hello, World!"

# Testing visa API calls
@app.route('/visa-api-test')
def visa_api_test():
    return visa_api_call('https://sandbox.api.visa.com/vdp/helloworld').content

# Testing visa API calls
def visa_push_funds(json):
    url = 'https://sandbox.api.visa.com/visadirect/fundstransfer/v1/pushfundstransactions'
    headers = {"Content-Type":"application/json", "Accept":"application/json"}
    x = visa_api_call(url, methodType=requests.post, headers=headers, json=json).json()
    return x

@app.route('/makePaymentOnInvoice', methods=['POST'])
def makePaymentOnInvoice():
    # json must have "senderPAN" and "invoiceId"
    sender_json = request.json
    if 'senderPAN' not in sender_json or 'invoiceId' not in sender_json:
        return {'status':'fail', 'result':'Missing required field(s) in POST body'}

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
        "amount": invoice['amount'],
        "recipientPrimaryAccountNumber": invoice['pan'],
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

def visa_api_call(url, methodType=requests.get, headers="", data="", **kw):
    user_id = os.getenv("userid")
    password = os.getenv("password")

    #verify = (certs_dir_path + '/DigiCertGlobalRootCA.crt'),
    r = methodType(url,
        verify = (""),
        cert = (certs_dir_path + '/visa-api/cert.pem',
                certs_dir_path + '/visa-api/key_54a11bcc-fab0-449d-9092-4fa83d6a557b.pem'),
        headers = headers,
        auth = (user_id, password),
        data = data,
        **kw
        )

    return r


if __name__ == '__main__': # pragma: no cover
    # Checks if we have environment variables set for our TLS keys (this is optional)
    fullchainpath = os.getenv("fullchainpath")
    privatekeypath = os.getenv("privatekeypath")
    if fullchainpath is not None and privatekeypath is not None:
        context = (fullchainpath, privatekeypath)
    else:
        context = None

    # Runs on port 5000, switch to whatever you like
    app.run("0.0.0.0", 5000, app, ssl_context=context)

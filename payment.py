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
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from firebase_admin import auth

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

def send_confirmation(email, data):
    # Send confirmation Email
    message = Mail(
        from_email='pandemic.coders@gmail.com',
        to_emails=email
    )
    message.dynamic_template_data = data
    message.template_id = 'd-2a96789c5f1c4ee5a612d632f7704937'
    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        response = sg.send(message)
    except Exception as e:
        print(e)

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
        assert doc.exists, 'Record doesn\'t exist with given invoiceId'
        invoice = doc.to_dict()

        # Check if the invoice has merchantId
        merchant_doc = None
        merchant_doc_ref = None
        if 'merchantId' in invoice:
            merchant_doc_ref = database.collection(u'merchants').document(invoice['merchantId'])
            merchant_doc = merchant_doc_ref.get()
            assert merchant_doc.exists, 'Invalid merchantId'
            invoice['email'] = auth.get_user(invoice['merchantId']).email
            del invoice['merchantId']
            invoice = dict(invoice, **merchant_doc.to_dict()['paymentInfo'])

        # Get the tip
        tip = 0 if 'tip' not in sender_json else sender_json['tip']

        # Get the date and audit number
        now = datetime.now()
        auditNumber = str(hash(sender_json['invoiceId']) % 1000000).zfill(6)
        retrievalReferenceNumber = now.strftime("%y")[1] + now.strftime("%j%H") + auditNumber
        # Build the push json to send
        api_json = {
            "amount": str(tip + sum([float(item['amount']) for item in invoice['items']])),
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
        pull_res_json = json.loads(pull_res.content)
        pull_res_err = str(pull_res_json)
        if 'errorMessage' in pull_res_json:
            pull_res_err = pull_res_json['errorMessage']

        assert pull_res.status_code == 200, '{\"senderPAN\":[\"Pull: '+ str(pull_res_err) +'\"]}'

        push_res = visa_push_funds(push_api_json)
        push_res_json = json.loads(push_res.content)
        push_res_err = str(push_res_json)
        if 'errorMessage' in push_res_json:
            push_res_err = push_res_json['errorMessage']
        assert push_res.status_code == 200, '{\"senderPAN\":[\"Push: '+ str(push_res_err) +'\"]}'

        data = {
            'invoiceId': code,
            'total': str(format(tip + sum([float(item['amount']) for item in invoice['items']]), ".2f")),
            'items': [{"amount":"%.2f" % item['amount'], "desc":item['desc']} for item in invoice['items']]
        }

        send_confirmation(invoice['email'], data)
        if 'email' in sender_json:    
            send_confirmation(sender_json['email'], data)
       
        # Add the tip to the total if they're signed in
        if merchant_doc_ref is not None and 'tip' in sender_json:
            currTotal = merchant_doc.to_dict()['tipsTotal']
            # issue: This could result in concurrent inconsistency
            merchant_doc_ref.update({'tipsTotal': currTotal + tip})

        return push_res.json()


''' invoices.py
Description of the purpose of this file
'''
from flask import jsonify, request
from flask_restful import Resource
from db import database
from db import InvoiceSchema
from db import InvoiceSignedinSchema
from helpers import decorate_all_methods, return_status
import random, string
import json
import threading, sched, time
from generator import TokenGenerator
from marshmallow import ValidationError
from firebase_admin import auth
from firebase_admin import firestore

# Helper functions
codeGenerator = TokenGenerator()

def generateDocRef():
    while True:
        code = codeGenerator.generate()
        new_invoice_ref = database.collection(u'invoices').document(code)
        new_invoice = new_invoice_ref.get()
        if not new_invoice.exists:
            return new_invoice_ref
        else:
            invoice_dict = new_invoice.to_dict()
            created = invoice_dict['created']
            difference = time.time() - created
            if difference > 86400:
                # delete the doc
                new_invoice_ref.delete()
                # create a new one again
                return database.collection(u'invoices').document(code)

scheduler = sched.scheduler(time.time, time.sleep)
def scheduleExpirationHandler(apiRef, userCode, timeUntilExpiration=60*60):
    scheduler.enter(timeUntilExpiration, 1, apiRef.delete, kwargs={'id':userCode})
    scheduler.run()

# Invoice RESTful resource Controller
@decorate_all_methods(return_status)
class Invoice(Resource):
    def get(self, id=None):
        doc_ref = database.collection(u'invoices').document(id)
        doc = doc_ref.get()
        assert doc.exists, 'failure'
        assert time.time() - doc.to_dict()['created'] <= 86400, 'expired'
        doc_dict = doc.to_dict()
        if 'additionalMessage' in doc_dict:
            additionalMessage = doc_dict['additionalMessage']
        else:
            additionalMessage = ""
        ret_obj = {
            'businessName': doc_dict['businessName'],
            'additionalMessage': additionalMessage,
            'items': doc_dict['items']
        }
        return {'nameOfId':id,
                'invoiceObj':ret_obj}

    def post(self, id=None):
        new_invoice_ref = generateDocRef()
        in_json = json.loads(request.data)
        if 'merchantToken' in in_json:
            result = InvoiceSchema().load(in_json)
        else:
            result = InvoiceSignedinSchema().load(in_json)
            decoded_token = auth.verify_id_token(result['merchantToken'])
            del result['merchantToken']
            result['merchantId'] = decoded_token['uid']
        result['created'] = time.time()
        new_invoice_ref.set(result)
        code = new_invoice_ref.id
        # Schedule the expiration
        t = threading.Thread(target=scheduleExpirationHandler, args=(self,code,))
        t.start()
        return {'invoiceCode': code}

    def delete(self, id=None):
        doc_ref = database.collection(u'invoices').document(id)
        doc_ref.delete()

    def put(self, id=None):
        doc_ref = database.collection(u'invoices').document(id)
        doc_ref.delete()
        doc_ref.set(json.loads(request.data))

    def patch(self, id=None):
        in_json = json.loads(request.data)
        assert in_json <= list(InvoicesSchema().__dict__.keys()), 'Invalid keys'
        doc_ref = database.collection(u'invoices').document(uid)
        doc_ref.update(in_json)

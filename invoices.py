''' invoices.py
Description of the purpose of this file
'''
from flask import jsonify, request
from flask_restful import Resource
from db import database
from db import InvoiceSchema
from helpers import decorate_all_methods, return_status
import random, string
import json
import threading, sched, time
from generator import TokenGenerator

# Helper functions
codeGenerator = TokenGenerator()

def generateDocRef():
    while True:
        code = codeGenerator.generate()
        new_invoice_ref = database.collection(u'invoices').document(code)
        if not new_invoice_ref.get().exists:
            return new_invoice_ref

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
        return {'nameOfId':id,
                'invoiceObj':doc.to_dict()}

    def post(self, id=None):
        new_invoice_ref = generateDocRef()
        result = InvoiceSchema().load(json.loads(request.data))
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
        doc_ref = database.collection(u'invoices').document(id)
        doc_ref.update(json.loads(request.data))

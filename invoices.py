''' invoices.py
Description of the purpose of this file
'''
from flask import jsonify, request
from flask_restful import Resource
from db import invoices
from db import database
from helpers import decorate_all_methods, return_status
import random, string
import json

# Helper functions TODO
def businessToUserCode(businessCode):
    return (userCode-1000)//2

def userToBusinessCode(userCode):
    return 2*userCode + 1000

# Invoice RESTful resource Controller
@decorate_all_methods(return_status)
class Invoice(Resource):
    def get(self, id=None):
        code = userToBusinessCode(id)
        doc_ref = database.collection(u'invoices').document(code)
        doc = doc_ref.get()
        assert doc.exists, 'failure'
        return {'nameOfId':id,
                'invoiceObj':doc.to_dict()}

    def post(self, id=None):
        new_invoice_ref = database.collection(u'invoices').document()
        new_invoice_ref.set(json.loads(request.data))
        return {'invoiceCode': businessToUserCode(new_invoice_ref.id)}

    def delete(self, id=None):
        code = userToBusinessCode(id)
        doc_ref = database.collection(u'invoices').document(code)
        doc_ref.delete()

    def put(self, id=None):
        code = userToBusinessCode(id)
        doc_ref = database.collection(u'invoices').document(code)
        doc_ref.delete()
        doc_ref.set(json.loads(request.data))

    def patch(self, id=None):
        code = userToBusinessCode(id)
        doc_ref = database.collection(u'invoices').document(code)
        doc_ref.update(json.loads(request.data))

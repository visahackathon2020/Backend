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

# Invoice RESTful resource Controller
@decorate_all_methods(return_status)
class Invoice(Resource):
    def get(self, id=None):
        return {'nameOfId':id,
                'invoiceObj':invoices[id]}

    def post(self, id=None):
        new_invoice_ref = database.collection(u"invoices").document()
        new_invoice_ref.set(json.loads(request.data))
        return {'invoiceCode': new_invoice_ref.id}

    def delete(self, id=None):
        del invoices[id]

    def put(self, id=None):
        invoices[id] = request.json

    def patch(self, id=None):
        invoices[id].update(request.json)

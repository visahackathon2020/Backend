''' invoices.py
Description of the purpose of this file
'''
from flask import jsonify, request
from flask_restful import Resource
from db import invoices
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
        # Generate unique id
        while True:
            id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
            if id not in invoices:
                break
        invoices[id] = json.loads(request.data)
        return {'invoiceCode':id}

    def delete(self, id=None):
        del invoices[id]

    def put(self, id=None):
        invoices[id] = request.json

    def patch(self, id=None):
        invoices[id].update(request.json)

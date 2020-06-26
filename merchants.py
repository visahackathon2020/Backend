''' merchants.py
Description of the purpose of this file
'''
from flask import jsonify, request
from flask_restful import Resource
from helpers import decorate_all_methods, return_status
import json
from db import database
from db import MerchantsSchema
from firebase_admin import auth
from functools import wraps

def check_headers(func):
    @wraps(func)
    def wrapper(*args, **kw):
        assert 'Authorization' in request.headers, 'Missing Authorization header'
        decoded_token = auth.verify_id_token(request.headers['Authorization'])
        uid = decoded_token['uid']
        return func(*args, uid=uid, **kw)
    return wrapper

# Merchants RESTful resource Controller
@decorate_all_methods(return_status)
@decorate_all_methods(check_headers)
class Merchant(Resource):
    # Check if merchant doc exist
    def get(self, uid=None):
        doc_ref = database.collection(u'merchants').document(uid)
        doc = doc_ref.get()
        return {'docExists':str(doc.exists)}

    # Create a merchant doc
    def post(self, uid=None):
        result = MerchantsSchema().load(json.loads(request.data))
        doc_ref = database.collection(u'merchants').document(uid)
        doc_ref.set(result)

    def delete(self, uid=None):
        doc_ref = database.collection(u'merchants').document(uid)
        doc_ref.delete()

    def put(self, uid=None):
        result = MerchantsSchema().load()
        doc_ref = database.collection(u'merchants').document(uid)
        doc_ref.delete()
        doc_ref.set(result)

    def patch(self, uid=None):
        in_json = json.loads(request.data)
        assert in_json <= list(MerchantsSchema().__dict__.keys()), 'Invalid keys'
        doc_ref = database.collection(u'merchants').document(uid)
        doc_ref.update(in_json)

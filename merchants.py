''' merchants.py
Description of the purpose of this file
'''
from flask import jsonify, request
from flask_restful import Resource
from helpers import decorate_all_methods, return_status
import json
from db import database
from firebase_admin import auth

# Merchants RESTful resource Controller
@decorate_all_methods(return_status)
class Merchant(Resource):
    def get(self, id=None):
        return None

    # Create a merchant info model
    def post(self, cmd=None):
        if cmd == "docExists":
            body = json.loads(request.data)
            decoded_token = auth.verify_id_token(body['authToken'])
            uid = decoded_token['uid']
            doc_ref = database.collection(u'merchants').document(uid)
            doc = doc_ref.get()
            assert doc.exists, 'Does not exist'
            return 'Exists'
        
        assert False, 'Invalid endpoint'

    def delete(self, id=None):
        return None

    def put(self, id=None):
        return None

    def patch(self, id=None):
        return None

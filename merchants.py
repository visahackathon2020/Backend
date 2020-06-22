''' merchants.py
Description of the purpose of this file
'''
from flask import jsonify, request
from flask_restful import Resource
from db import merchants
from helpers import decorate_all_methods, return_status

# Merchants RESTful resource Controller
@decorate_all_methods(return_status)
class Merchant(Resource):
    def get(self, id=None):
        return None

    # Create a merchant info model
    def post(self, id=None):
        return None

    def delete(self, id=None):
        return None

    def put(self, id=None):
        return None

    def patch(self, id=None):
        return None

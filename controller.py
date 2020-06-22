#!flask/bin/python
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, fields, marshal
from flask_cors import CORS, cross_origin
import requests
import os
import sys
from dotenv import load_dotenv
import random, string
from helpers import decorate_all_methods
from functools import wraps


load_dotenv() # Load environment variables
certs_dir_path = os.path.dirname(os.path.realpath(__file__)) + '/certs' # path to our certs

app = Flask(__name__)
api = Api(app)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Origin'] = '*'
    return response

# Fake database mock
invoices = {'1':{'merchantid':'12345678900000000000000000000000','amount':'10','items':[{'name':'taco','price':'10','quantity':'1'}]},
            '2':{'merchantid':'22222222222222222222222222222222','amount':'6.28','items':[{'name':'fries','price':'3.14','quantity':'2'}]},
            '3':{'name':'Ben','bin':'1234','pan':'33333333333333333333333333333333','country':'us','amount':'6.28','items':[{'name':'fries','price':'3.14','quantity':'2'}]}}
merchants = {'12345678900000000000000000000000':{'token':'44444444444444444444444444444444'},
             '22222222222222222222222222222222':{'token':'55555555555555555555555555555555'}}

# Schemas
item_fields = {
    'name': fields.String,
    'price': fields.String,
    'quantity': fields.String
}

merchant_info_fields = {
    'name': fields.String,
    'country': fields.String,
    'BIN': fields.String,
    'PAN': fields.String
}

invoice_with_account_fields = {
    'merchantid': fields.String,
    'amount': fields.String,
    'items': fields.List(fields.Nested(item_fields))
}

invoice_no_account_fields = {
    'name': fields.String,
    'country': fields.String,
    'BIN': fields.String,
    'PAN': fields.String,
    'amount': fields.String,
    'items': fields.List(fields.Nested(item_fields))
}

# This wraps the resource class methods and returns the standard response
def return_status(func):
    @wraps(func)
    def wrapper(*args, **kw):
        try:
            res = func(*args, **kw)
            status = 'success'
        except:
            status = 'fail'
            res = ''
        finally:
            id = '' if 'id' not in kw else str(kw['id'])
            return {'method':func.__name__.upper(), 'status':status, 'id':id, 'result':'' if res is None else res}
    return wrapper


# Merchants RESTful resource Controller
@api.resource('/merchants', '/merchants/<string:id>')
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

# Invoice RESTful resource Controller
@api.resource('/invoices', '/invoices/<string:id>')
@decorate_all_methods(return_status)
class Invoice(Resource):
    def get(self, id=None):
        return {id: invoices[id]}

    def post(self, id=None):
        # Generate unique id
        while True:
            id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
            if id not in invoices:
                break
        # Check that the data is in any valid form
        invoices[id] = request.json
        return {'invoiceCode':id}

    def delete(self, id=None):
        del invoices[id]

    def put(self, id=None):
        invoices[id] = request.json

    def patch(self, id=None):
        invoices[id].update(request.json)

# Testing Flask
@app.route('/')
def index():
    return "Hello, World!"

# Testing visa API calls
@app.route('/visa-api-test')
def visa_api_test():
    return visa_api_call('https://sandbox.api.visa.com/vdp/helloworld').content

def visa_api_call(url, methodType=requests.get, data=""):
    user_id = os.getenv("userid")
    password = os.getenv("password")
    headers = ""
    data = data

    #verify = (certs_dir_path + '/DigiCertGlobalRootCA.crt'),
    r = methodType(url,
        verify = (""),
        cert = (certs_dir_path + '/visa-api/cert.pem',
                certs_dir_path + '/visa-api/key_54a11bcc-fab0-449d-9092-4fa83d6a557b.pem'),
        headers = headers,
        auth = (user_id, password),
        data = data,
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

    # Runs on port 80, switch to whatever you like
    app.run("0.0.0.0", 5000, app, ssl_context=context)

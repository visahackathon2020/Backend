#!flask/bin/python
from flask import Flask, jsonify, request
from flask_restful import Resource, Api, fields, marshal
import requests
import os
import sys
from dotenv import load_dotenv
import random, string


load_dotenv() # Load environment variables
certs_dir_path = os.path.dirname(os.path.realpath(__file__)) + '/certs' # path to our certs

app = Flask(__name__)
api = Api(app)

# Fake database mock
invoices = {'1':{'name':'Nikhil','token':'12345678900000000000000000000000','amount':'10','items':[{'name':'taco','price':'10','quantity':'1'}]},
            '2':{'name':'Ben','token':'12345678900000000000000000000000','amount':'6.28','items':[{'name':'fries','price':'3.14','quantity':'2'}]}}
merchants = {}

# Argument parsers
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

invoice_fields = {
    'name': fields.String,
    'token': fields.String,
    'amount': fields.String,
    'items': fields.List(fields.Nested(item_fields))
}

# Merchants RESTful resource Controller
@api.resource('/merchants', '/merchants/<string:id>')
class Merchant(Resource):
    def get(self, id=None):
        return {"method":"GET","status":"fail","id": id}

    # Create a merchant info model
    def post(self, id=None):
        try:
            merchants[id] = request.json
        except:
            return {"method":"POST","status":"fail","id": id}
        return {"method":"POST","status":"success","id": id}

    def delete(self, id=None):
        return {"method":"DELETE","status":"fail","id": id}

    def put(self, id=None):
        return {"method":"PUT","status":"fail","id": id}

    def patch(self, id=None):
        return {"method":"PATCH","status":"fail","id": id}

# Invoice RESTful resource Controller
@api.resource('/invoices', '/invoices/<string:id>')
class Invoice(Resource):
    def get(self, id=None):
        try: return {id: invoices[id]}
        except: return {"method":"GET","status":"fail","id": id}

    def post(self, id=None):
        # Generate unique id
        while True:
            test_id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
            if test_id not in invoices:
                break
        try:
            invoices[test_id] = request.json
        except: return {"method":"POST","status":"fail","id": test_id}
        return {"method":"POST","status":"success","id": test_id}

    def delete(self, id=None):
        try:
            del invoices[id]
        except: return {"method":"DELETE","status":"fail","id": id}
        return {"method":"DELETE","status":"success","id": id}

    def put(self, id=None):
        try: invoices[id] = request.json
        except: return {"method":"PUT","status":"fail","id": id}
        return {"method":"PUT","status":"success","id": id}

    def patch(self, id=None):
        try: invoices[id].update(request.json)
        except: return {"method":"PATCH","status":"fail","id": id, "msg":str(sys.exc_info())}
        return {"method":"PATCH","status":"success","id": id}

# Testing Flask
@app.route('/')
def index():
    return "Hello, World!"
@app.route('/hello-world')
def hello_world():
    return "Hello, World!"

# Testing visa API calls
@app.route('/visa-api-test')
def visa_api_test():
    url = 'https://sandbox.api.visa.com/vdp/helloworld'
    user_id = os.getenv("userid")
    password = os.getenv("password")
    headers = ""
    body = ""

    #verify = (certs_dir_path + '/DigiCertGlobalRootCA.crt'),
    r = requests.get(url,
        verify = (""),
        cert = (certs_dir_path + '/visa-api/cert.pem',
                certs_dir_path + '/visa-api/key_54a11bcc-fab0-449d-9092-4fa83d6a557b.pem'),
        headers = headers,
        auth = (user_id, password),
        data = body)

    return r.content


if __name__ == '__main__':
    # Checks if we have environment variables set for our TLS keys (this is optional)
    fullchainpath = os.getenv("fullchainpath")
    privatekeypath = os.getenv("privatekeypath")
    if fullchainpath is not None and privatekeypath is not None:
        context = (fullchainpath, privatekeypath)
    else:
        context = None

    # Runs on port 80, switch to whatever you like
    app.run("0.0.0.0", 80, app, ssl_context=context)

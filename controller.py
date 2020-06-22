#!flask/bin/python
''' controller.py
Description of the purpose of this file
'''
from flask import Flask
from flask_restful import Api
from flask_cors import CORS, cross_origin
import requests
import os
import sys
from dotenv import load_dotenv


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

import invoices
import merchants

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

    # Runs on port 5000, switch to whatever you like
    app.run("0.0.0.0", 5000, app, ssl_context=context)

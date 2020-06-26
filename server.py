#!flask/bin/python
''' server.py
Description of the purpose of this file
'''
from flask import Flask, request
from flask_restful import Api
from flask_cors import CORS, cross_origin
import requests
import os
import sys
from dotenv import load_dotenv
import json
from datetime import datetime
from db import database

from visa_api import visa_api_call

load_dotenv() # Load environment variables

app = Flask(__name__)
api = Api()
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

@app.after_request
def after_request(response):
    header = response.headers
    header['Access-Control-Allow-Methods'] = '*'
    header['Access-Control-Allow-Headers'] = '*'
    header['Access-Control-Allow-Origin'] = '*'
    return response

from invoices import Invoice
from merchants import Merchant
from payment import Payment
api.add_resource(Invoice,'/invoices','/invoices/', '/invoices/<string:id>')
api.add_resource(Merchant,'/merchants','/merchants/')
api.add_resource(Payment, '/payment')
api.init_app(app)

# Testing Flask
@app.route('/')
def index():
    return "Hello, World!"

# Testing visa API calls
@app.route('/visa-api-test')
def visa_api_test():
    return visa_api_call('https://sandbox.api.visa.com/vdp/helloworld').content

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

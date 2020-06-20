#!flask/bin/python
from flask import Flask, jsonify, request
from werkzeug import serving
from OpenSSL import SSL
import requests
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables
app = Flask(__name__)
certs_dir_path = os.path.dirname(os.path.realpath(__file__)) + '/certs'

@app.route('/')
def index():
    return "Hello, World!"

@app.route('/foo', methods=['POST'])
def json_post_test():
    data = request.json
    return jsonify(data)

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
    ssl_context = (certs_dir_path + '/server.crt',certs_dir_path + '/server.key')
    fullchainpath = os.getenv("fullchainpath")
    privatekeypath = os.getenv("privatekeypath")
    if fullchainpath is not None and privatekeypath is not None:
        context = (fullchainpath, privatekeypath)
    else:
        context = None

    app.run("0.0.0.0", 80, app, ssl_context=context)

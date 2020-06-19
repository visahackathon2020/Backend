#!flask/bin/python
from flask import Flask, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv() # Load environment variables
app = Flask(__name__)
certs_dir_path = os.path.dirname(os.path.realpath(__file__)) + '/certs'

@app.route('/hello-world')
def hello_world():
    return "Hello, World!"

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
        cert = (certs_dir_path + '/cert.pem',certs_dir_path + '/key_54a11bcc-fab0-449d-9092-4fa83d6a557b.pem'),
        headers = headers,
        auth = (user_id, password),
        data = body)

    return r.content

if __name__ == '__main__':
    #app.run(debug=True,ssl_context=(certs_dir_path + '/server.crt',certs_dir_path + '/server.key'))
    app.run(debug=True,ssl_context='adhoc')

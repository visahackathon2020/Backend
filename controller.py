#!flask/bin/python
from flask import Flask
import requests
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/hello-world')
def hello_world():
    return "Hello, World!"

@app.route('/visa-api-test')
def visa_api_test():
    url = 'https://sandbox.api.visa.com/vdp/helloworld'
    dir_path = os.path.dirname(os.path.realpath(__file__))
    user_id = os.getenv("userid")
    password = os.getenv("password")
    headers = ""
    body = ""

    #verify = (dir_path + '/DigiCertGlobalRootCA.crt'),
    r = requests.get(url,
        verify = (""),
        cert = (dir_path + '/cert.pem',dir_path + '/key_54a11bcc-fab0-449d-9092-4fa83d6a557b.pem'),
        headers = headers,
        auth = (user_id, password),
        data = body)

    return r.content

if __name__ == '__main__':
    app.run(debug=True)

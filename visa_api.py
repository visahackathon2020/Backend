import os
import requests

certs_dir_path = os.path.dirname(os.path.realpath(__file__)) + '/certs' # path to our certs

def visa_api_call(url, methodType=requests.get, headers="", data="", **kw):
    user_id = os.getenv("userid")
    password = os.getenv("password")

    #verify = (certs_dir_path + '/DigiCertGlobalRootCA.crt'),
    r = methodType(url,
        verify = (""),
        cert = (certs_dir_path + '/visa-api/cert.pem',
                certs_dir_path + '/visa-api/key_54a11bcc-fab0-449d-9092-4fa83d6a557b.pem'),
        headers = headers,
        auth = (user_id, password),
        data = data,
        **kw
        )

    return r
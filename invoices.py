''' invoices.py
Description of the purpose of this file
'''
from flask import jsonify, request
from flask_restful import Resource
from db import invoices
from db import database
from helpers import decorate_all_methods, return_status
import random, string
import json
import threading, sched, time

# Helper functions
userCodes = {}
def businessToUserCode(businessCode):
    while True:
        code = ''.join([str(random.randint(0,9)) for _ in range(6)])
        if code not in userCodes:
            break
    userCodes[code] = businessCode
    return code

def userToBusinessCode(userCode):
    return userCodes[userCode]

scheduler = sched.scheduler(time.time, time.sleep)
def scheduleExpirationHandler(apiRef, userCode, timeUntilExpiration=60*60):
    scheduler.enter(timeUntilExpiration, 1, apiRef.delete, kwargs={'id':userCode})
    scheduler.run()

# Invoice RESTful resource Controller
@decorate_all_methods(return_status)
class Invoice(Resource):
    def get(self, id=None):
        code = userToBusinessCode(id)
        doc_ref = database.collection(u'invoices').document(code)
        doc = doc_ref.get()
        assert doc.exists, 'failure'
        return {'nameOfId':id,
                'invoiceObj':doc.to_dict()}

    def post(self, id=None):
        new_invoice_ref = database.collection(u'invoices').document()
        new_invoice_ref.set(json.loads(request.data))
        code = businessToUserCode(new_invoice_ref.id)
        # Schedule the expiration
        t = threading.Thread(target=scheduleExpirationHandler, args=(self,code,))
        t.start()
        return {'invoiceCode': code}

    def delete(self, id=None):
        code = userToBusinessCode(id)
        doc_ref = database.collection(u'invoices').document(code)
        doc_ref.delete()
        del userCodes[id]

    def put(self, id=None):
        code = userToBusinessCode(id)
        doc_ref = database.collection(u'invoices').document(code)
        doc_ref.delete()
        doc_ref.set(json.loads(request.data))

    def patch(self, id=None):
        code = userToBusinessCode(id)
        doc_ref = database.collection(u'invoices').document(code)
        doc_ref.update(json.loads(request.data))

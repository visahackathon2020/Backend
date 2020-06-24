''' db.py
'''
from flask_restful import fields
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("./certs/firebase/phonepayhack-firebase-adminsdk-ovw0a-fdd73540c4.json")
firebase_admin.initialize_app(cred)

database = firestore.client()

# Fake database mock
invoices = {'1':{'name':'Kyle','merchantid':'12345678900000000000000000000000','items':[{'invoiceAmt':'10','invoiceDesc':'1 taco for 10 dollars'}]},
            '2':{'name':'Eric','merchantid':'22222222222222222222222222222222','items':[{'invoiceAmt':'3.14','invoiceDesc':'1 fries for 3.14 dollars'}]},
            '3':{'name':'Ben','bin':'1234','pan':'33333333333333333333333333333333','country':'us','items':[{'invoiceAmt':'3.14','invoiceDesc':'1 fries for 3.14 dollars'}]}}
merchants = {'12345678900000000000000000000000':{'token':'44444444444444444444444444444444'},
             '22222222222222222222222222222222':{'token':'55555555555555555555555555555555'}}

item_fields = {
    'invoiceAmt': fields.String,
    'invoiceDesc': fields.String
}

merchant_info_fields = {
    'name': fields.String,
    'country': fields.String,
    'BIN': fields.String,
    'PAN': fields.String
}

# This is supposed to eventually be for filtering the inputs to the POST invoices call
invoice_input_fields = {
    'name': fields.String,

    'country': fields.String,
    'state': fields.String,
    'zipcode': fields.String,

    'BIN': fields.String,
    'PAN': fields.String,
    'items': fields.List(fields.Nested(merchant_info_fields))
}

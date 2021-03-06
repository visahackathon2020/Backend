''' db.py
'''
import firebase_admin
import re
from firebase_admin import credentials
from firebase_admin import firestore

from marshmallow import Schema, fields, validate, validates, ValidationError

cred = credentials.Certificate("./certs/firebase/phonepayhack-firebase-adminsdk-ovw0a-fdd73540c4.json")
firebase_admin.initialize_app(cred)

database = firestore.client()

# Fake database mock
# invoices = {'1':{'name':'Kyle','merchantid':'12345678900000000000000000000000','items':[{'invoiceAmt':'10','invoiceDesc':'1 taco for 10 dollars'}]},
#             '2':{'name':'Eric','merchantid':'22222222222222222222222222222222','items':[{'invoiceAmt':'3.14','invoiceDesc':'1 fries for 3.14 dollars'}]},
#             '3':{'name':'Ben','bin':'1234','pan':'33333333333333333333333333333333','country':'us','items':[{'invoiceAmt':'3.14','invoiceDesc':'1 fries for 3.14 dollars'}]}}
# merchants = {'12345678900000000000000000000000':{'token':'44444444444444444444444444444444'},
#              '22222222222222222222222222222222':{'token':'55555555555555555555555555555555'}}

class ItemSchema(Schema):
    amount = fields.Float(required=True)
    desc = fields.Str(required=True)

    @validates('amount')
    def validate_amount(self, value):
        if value < 0:
            raise ValidationError('Amout must be greater than 0')

# merchant_info_fields = {
#     'name': fields.String,
#     'country': fields.String,
#     'BIN': fields.String,
#     'PAN': fields.String
# }

# This is supposed to eventually be for filtering the inputs to the POST invoices call
class MerchantsSchema(Schema):
    name = fields.Str(required=True, error_messages={"required": "name is required."})
    country = fields.Str(required=True, error_messages={"required": "country is required."})
    state = fields.Str(required=True, error_messages={"required": "state is required."})
    zipcode = fields.Str(required=True, error_messages={"required": "zipcode is required."})
    PAN = fields.Str(required=True, error_messages={"required": "PAN is required."})

    @validates('PAN')
    def validate_pan(self, value):
        pattern = re.compile(r'\d{16}')
        if not pattern.match(value):
            raise ValidationError('Invalid PAN number')

class InvoiceSignedinSchema(Schema):
    businessName = fields.Str(required=True, error_messages={"required": "businessName is required."})
    additionalMessage = fields.Str()
    email = fields.Email(required=True, error_messages={"required": "email is required"})
    merchantToken = fields.Str(required=True, error_messages={"required": "merchantToken is required."})
    items = fields.List(fields.Nested(ItemSchema), required=True)

class InvoiceSchema(Schema):
    def validate_pan(self, value):
        pattern = re.compile()
        if not pattern.match(value):
            raise ValidationError('Invalid PAN number')

    def validate_email(value):
        pattern = re.compile()
        if not pattern.match(value):
            raise ValidationError('Invalid Email Address')

    businessName = fields.Str(required=True, error_messages={"required": "businessName is required."})
    additionalMessage = fields.Str()
    emailRegEx = r'^([a-zA-Z0-9_\-\.]+)@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.)|(([a-zA-Z0-9\-]+\.)+))([a-zA-Z]{2,4}|[0-9]{1,3})(\]?)$'
    email = fields.Email(required=True, error_messages={"required": "email is required"})
    name = fields.Str(required=True, error_messages={"required": "name is required."})
    country = fields.Str(required=True, error_messages={"required": "country is required."})
    state = fields.Str(required=True, error_messages={"required": "state is required."})
    zipcode = fields.Str(required=True, error_messages={"required": "zipcode is required."})
    PAN = fields.Str(required=True, error_messages={"required": "PAN is required."}, validate=validate.Length(min=13,max=19))
    items = fields.List(fields.Nested(ItemSchema), required=True)


class PaymentSchema(Schema):
    senderPAN = fields.Str(required=True, validate=validate.Length(min=13,max=19))
    tip = fields.Float()
    invoiceId = fields.Str(required=True)
    email = fields.Email()

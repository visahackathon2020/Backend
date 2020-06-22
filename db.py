''' db.py
'''
from flask_restful import fields

# Fake database mock
invoices = {'1':{'merchantid':'12345678900000000000000000000000','amount':'10','items':[{'name':'taco','price':'10','quantity':'1'}]},
            '2':{'merchantid':'22222222222222222222222222222222','amount':'6.28','items':[{'name':'fries','price':'3.14','quantity':'2'}]},
            '3':{'name':'Ben','bin':'1234','pan':'33333333333333333333333333333333','country':'us','amount':'6.28','items':[{'name':'fries','price':'3.14','quantity':'2'}]}}
merchants = {'12345678900000000000000000000000':{'token':'44444444444444444444444444444444'},
             '22222222222222222222222222222222':{'token':'55555555555555555555555555555555'}}

# Schemas
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

invoice_with_account_fields = {
    'merchantid': fields.String,
    'amount': fields.String,
    'items': fields.List(fields.Nested(item_fields))
}

invoice_no_account_fields = {
    'name': fields.String,
    'country': fields.String,
    'BIN': fields.String,
    'PAN': fields.String,
    'amount': fields.String,
    'items': fields.List(fields.Nested(item_fields))
}

''' helper.py
Description of the purpose of this file
'''
from functools import wraps
import sys
import logging
import traceback
import json
from marshmallow import ValidationError
logger = logging.Logger('catch_all')

# This decorates all the methods of a class
def decorate_all_methods(function_decorator):
    def decorator(cls):
        for name, obj in vars(cls).items():
            if callable(obj):
                setattr(cls, name, function_decorator(obj))
        return cls
    return decorator

# This wraps the resource class methods and returns the standard response
def return_status(func):
    @wraps(func)
    def wrapper(*args, **kw):
        status = 'fail'
        res = None
        try:
            res = func(*args, **kw)
            status = 'success'
        except AssertionError as e:
            status = 'fail'
            logger.error(e, exc_info=True)
            try:
                msg = json.loads(str(e))
            except:
                msg = str(e)
            res = {'errorType': str(e.__class__.__name__),
                   'errorMessage': msg,
                   'traceback' : str(traceback.format_stack())}
        except ValidationError as e:
            status = 'fail'
            logger.error(e, exc_info=True)
            print(e.messages)
            res = {'errorType': str(e.__class__.__name__),
                   'errorMessage': e.messages,
                   'traceback' : str(traceback.format_stack())}
        except:
            print("here")
            ex_type, ex_value, ex_traceback = sys.exc_info()
            trace_back = traceback.extract_tb(ex_traceback)
            trace_back_res = ["File : %s , Line : %d, Func.Name : %s, Message : %s" % (i[0], i[1], i[2], i[3]) for i in trace_back]
            res = {'errorType': str(ex_type.__name__),
                   'errorMessage': str(ex_value),
                   'traceback' : trace_back_res}
        finally:
            id = '' if 'id' not in kw else str(kw['id'])
            return {'method':func.__name__.upper(), 'status':status, 'id':id, 'result':'' if res is None else res}
    return wrapper


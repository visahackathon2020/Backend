''' helper.py
Description of the purpose of this file
'''
from functools import wraps
import sys

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
        try:
            res = func(*args, **kw)
            status = 'success'
        except:
            status = 'fail'
            res = str(sys.exc_info())
        finally:
            id = '' if 'id' not in kw else str(kw['id'])
            return {'method':func.__name__.upper(), 'status':status, 'id':id, 'result':'' if res is None else res}
    return wrapper


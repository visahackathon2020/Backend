''' helper.py
Description of the purpose of this file
'''
from functools import wraps
import sys
import logging
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
        try:
            res = func(*args, **kw)
            status = 'success'
        except ValidationError as e:
            status = 'fail'
            logger.error(e, exc_info=True)
            res = 'Invalid input: ' + str(e)
        except Exception as e:
            status = 'fail'
            logger.error(e, exc_info=True)
            res = str(e)
        except:
            res = str(sys.exc_info())
        finally:
            id = '' if 'id' not in kw else str(kw['id'])
            return {'method':func.__name__.upper(), 'status':status, 'id':id, 'result':'' if res is None else res}
    return wrapper


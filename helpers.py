# This decorates all the methods of a class
def decorate_all_methods(function_decorator):
    def decorator(cls):
        for name, obj in vars(cls).items():
            if callable(obj):
                setattr(cls, name, function_decorator(obj))
        return cls
    return decorator

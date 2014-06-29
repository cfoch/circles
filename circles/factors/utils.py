import functools

import factory


def factor_set_weight(weight):
    """
    It is just a decorator.
    """
    def decorator(factor_function):
        @functools.wraps(factor_function)
        def wrapper(*args, **kwargs):
            factor = factor_function(*args, **kwargs)
            return {"value": factor, "weight": weight}
        return wrapper
    return decorator


def valid_factor_name(name):
    """
    Validate method exists and starts with "factor_".
    """
    FACTOR_PREFIX = "factor_"
    obj = factory.FactorFunctionsFactory
    attr_names = dir(obj)
    if name not in attr_names:
        return False
    attr = getattr(obj, name)
    if not callable(attr):
        return False
    return name.startswith(FACTOR_PREFIX)

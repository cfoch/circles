from factors.factory import FactorFunctionsFactory


def valid_factor_name(name):
    """
    Validate method exists and starts with "factor_".
    """
    FACTOR_PREFIX = "factor_"
    obj = FactorFunctionsFactory
    attr_names = dir(obj)
    if name not in attr_names:
        return False
    attr = getattr(obj, name)
    if not callable(attr):
        return False
    return name.startswith(FACTOR_PREFIX)

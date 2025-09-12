"""Environment variable parsing helper functions"""

from os import environ


# environment variable values that represent "true"
TRUE_VALS = ["yes", "y", "true", "1", "t"]


def get_int(var_name: str, default: int) -> int:
    """Get integer environment variable value"""
    return int(environ.get(var_name, default))


def get_bool(var_name: str, default: bool) -> bool:
    """Get boolean environment variable value"""
    val = environ.get(var_name, default)

    if type(val) is not bool:
        return environ.get(var_name, default).lower() in TRUE_VALS
    return val

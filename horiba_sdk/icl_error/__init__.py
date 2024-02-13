"""
icl_error

A package that provides error handling for the ICL.

Errors comming from the ICL have the following format: `"[E];<error code>;<error string>"`. A list of known ICL errors
exists in the `error_list.json` file. Each error is defined by:

- number: the error code
- text: the text to be logged or put in an exception
- level: the level of severity

There is an internal mapping between the `level` defined in the json file and the internal horiba_sdk.icl_error.Severity
enum. This mapping exists because the library uses loguru as a logger lib, which has other names for the logging
severities.

"""

# Necessary to make Python treat the directory as a package
from .abstract_error import AbstractError, FakeError, Severity, StringAsSeverity
from .abstract_error_db import AbstractErrorDB, FakeErrorDB
from .icl_error import ICLError
from .icl_error_db import ICLErrorDB

__all__ = [
    'AbstractError',
    'AbstractErrorDB',
    'FakeError',
    'FakeErrorDB',
    'ICLError',
    'ICLErrorDB',
    'Severity',
    'StringAsSeverity',
]

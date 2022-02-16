from jsonschema import validate
from flask import request
from functools import wraps
from constants import json_schema
from constants.error_lib import BackEndException, ErrorMessages, ErrorCodes


def validate_payload(func):
    '''
    : Returns a USER_NOT_AUTHORIZED_ERROR if the input JWT
    : is not the JWT of a student user.
    '''
    @wraps(func)
    def wrapper():
        payload = request.get_json()
        if payload is None:
            raise BackEndException(
                ErrorMessages.BAD_DATA,
                ErrorCodes.BAD_REQUEST)
        try:
            validate(instance=payload, schema=json_schema)
        except:
            raise BackEndException(
                ErrorMessages.VALIDATION_FAILED,
                ErrorCodes.BAD_REQUEST
            )

        return func(payload)
    return wrapper

from functools import wraps
import jwt
from jwt import PyJWKClient
from flask import request
from constants.jwt_constants import JWT_CONSTANTS
from constants.error_lib import BackEndException, ErrorMessages, ErrorCodes


def get_signing_key(token):
    jwks_client = PyJWKClient(JWT_CONSTANTS.JWKS_URL)
    return jwks_client.get_signing_key_from_jwt(token)


def verify_user(func):
    @wraps(func)
    def wrapper(plan_id=None):
        auth_token = request.headers.get(JWT_CONSTANTS.JWT)
        if auth_token is None:
            raise BackEndException(
                ErrorMessages.JWT_MISSING,
                ErrorCodes.UNAUTHORIZED)
        try:
            signing_key = get_signing_key(auth_token)

            jwt.decode(
                auth_token,
                signing_key.key,
                algorithms=[JWT_CONSTANTS.ALG],
                audience=JWT_CONSTANTS.AUD,
                verify_exp=True)
        except Exception:
            raise BackEndException(
                ErrorMessages.USER_NOT_AUTHORIZED,
                ErrorCodes.UNAUTHORIZED)
        if plan_id is None:
            return func()
        return func(plan_id)
    return wrapper

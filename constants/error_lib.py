"""
: Error util library for constant error messages and error codes.
"""


class BackEndException(Exception):
    """
    : Class that wraps an error exception to return to HTTP clients.
    """
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        """
        : returns the dictionary representation of this error.
        """
        response_dict = dict(self.payload or {})
        response_dict['message'] = self.message
        response_dict['error'] = True
        return response_dict


class ErrorCodes:
    """
    : Enumerated error code wrapper class.
    """
    OK = 200
    USER_CREATED = 201
    EMPTY_CONTENT = 204
    NOT_CHANGED = 304
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICTED = 409
    SERVER_ERROR = 500


class ErrorMessages:
    """
    : Error message constants.
    """
    MISSING_USER_AUTH = 'User authorization info not provided.'
    def user_not_found_error(user_id):
        if user_id is None:
            return MISSING_USER_AUTH
        return 'User with user name/email ' + user_id + ' does not exist'

    USER_NOT_AUTHORIZED = 'Current user is not authorized to access or change this information'
    USER_NOT_AUTHENTICATED = 'Bad authentication token passed in'
    DUPLICATED_EMAIL = 'The given email address already exists, please try another one'

    JWT_MISSING = 'Authentication token is missing'
    INVALID_PASSWORD = 'Invalid email or password'
    INSECURE_PASSWORD = 'Password set is not secure'
    USER_CREATED = 'user created'

    SUCCESS = 'success'
    BAD_DATA = 'The given data from the request contains invalid data field(s) or some data fields required are missing'
    VALIDATION_FAILED = 'The given data from the request does not pass validation'
    CONTENT_NOT_CHANGED = 'The given data from the request has not changed from the previous call'

    UNABLE_DELETE = 'Unable to delete this file at this time. Please try again.'
    INVALID_FILE = 'This file name is invalid'
    PLAN_NOT_FOUND = 'Given plan not found'
    SERVICE_NOT_FOUND = 'Given service not found'
    MEMBER_COST_SHARE_NOT_FOND = 'Given member cost share not found'

    UNABLE_UPLOAD_IMAGE = 'Unable to upload image. Please try again'
    BOOK_ALREADY_EXISTS = 'This book is already created by someone.'

    BAD_DYNAMO_PAYLOAD = 'The given object is not an instance of BaseDynamoModel'


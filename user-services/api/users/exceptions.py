"""
    Custom Exception
    ___________________
"""
from rest_framework.exceptions import APIException


class FailedRegistrationException(APIException):
    """ Raised when something went registering user"""

    status_code = 422
    detail = "FAILED_REGISTRATION"

    def __init__(self, detail=None):
        if detail is not None:
            self.detail = detail


class OldMsisdnException(APIException):
    """ Raised when something tried updating new msisdn using old msisdn """

    status_code = 422
    detail = "OLD_MSISDN"

    def __init__(self, detail=None):
        if detail is not None:
            self.detail = detail


class UserNotFoundException(APIException):
    """ Raised when user still flagged as inactive (is_active = false) """

    status_code = 404
    detail = "USER_NOT_FOUND"

    def __init__(self, detail=None):
        if detail is not None:
            self.detail = detail

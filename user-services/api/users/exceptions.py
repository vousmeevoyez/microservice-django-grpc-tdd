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


class InvalidCredentialsException(APIException):
    """ Raised when something went user enter wrong credentials"""

    status_code = 401
    detail = "INVALID_CREDENTIALS"

    def __init__(self, detail=None):
        if detail is not None:
            self.detail = detail


class InactiveUserException(APIException):
    """ Raised when user still flagged as inactive (is_active = false) """

    status_code = 401
    detail = "INACTIVE_USER"

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


class OtpNotFoundException(APIException):
    """ Raised when otp is not found """

    status_code = 404
    detail = "OTP_NOT_FOUND"

    def __init__(self, detail=None):
        if detail is not None:
            self.detail = detail


class PendingOtpException(APIException):
    """ Raised when there's pending otp """

    status_code = 422
    detail = "PENDING_OTP"

    def __init__(self, detail=None):
        if detail is not None:
            self.detail = detail


class InvalidOtpException(APIException):
    """ Raised when invalid otp is entered """

    status_code = 422
    detail = "INVALID_OTP"

    def __init__(self, detail=None):
        if detail is not None:
            self.detail = detail

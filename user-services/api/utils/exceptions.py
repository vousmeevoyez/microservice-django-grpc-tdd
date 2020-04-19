"""
    Handling custom exception here
    _________________________
"""
from rest_framework.views import exception_handler
from rest_framework.exceptions import APIException

def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Now add the HTTP status code to the response.
    # if response is not None:
    #    response.data['status_code'] = response.status_code

    return response


class RemoteCallException(APIException):
    """ Raised when something went wrong executing remote call to external
    party """

    status_code = 422
    detail = "REMOTE_CALL_FAILED"

    def __init__(self, detail=None):
        self.detail = detail

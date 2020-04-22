"""
    Otp Views
"""
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.response import Response

from api.auths.services.otp import OtpService


class ResendOTPView(APIView):
    """
        POST /otp/resend
        __________________________
        Handle request to reset OTP
    """

    def post(self, request, user_id):
        response = OtpService(user_id=user_id).resend()
        return Response(response)

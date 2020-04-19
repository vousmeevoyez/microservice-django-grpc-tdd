"""
    Otp Views
"""
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.response import Response

from api.users.services import resend_user_otp


class ResendOTPView(APIView):

    def post(self, request, user_id):
        otp_id = resend_user_otp(user_id)
        response = {"otp": {"id": otp_id}}
        return Response(response, status=HTTP_204_NO_CONTENT)

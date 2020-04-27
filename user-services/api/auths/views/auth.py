"""
    Auth Views
"""
from rest_framework.status import HTTP_204_NO_CONTENT, HTTP_202_ACCEPTED
from rest_framework.views import APIView
from rest_framework.response import Response

from api.auths.serializers import LoginSerializer, ForgotPasswordSerializer
from api.auths.services.auth import (
    login,
    logout,
    request_reset_password,
    reset_password,
)


class LoginView(APIView):
    """
        POST /auth/login
        _____________________
        handle login using username and password will return JWT
    """

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response = login(**serializer.data)
            return Response(response)


class LogoutView(APIView):
    """
        POST /auth/logoout
        _____________________
        handle logout using JWT
    """

    def post(self, request):
        response = logout(request.user.id)
        return Response(response, status=HTTP_204_NO_CONTENT)


class RequestForgotPasswordView(APIView):
    """
        POST /auth/forgot/request
        _____________________
        handle requesting to forgot password will trigger sending otp to user
        next api is the one actually reset the user password
        there's celery task involved that's why we return 202 instead of 200
    """

    def post(self, request, user_id):
        response = request_reset_password(user_id)
        return Response(response, status=HTTP_202_ACCEPTED)


class VerifyForgotPasswordView(APIView):
    """
        POST /auth/forgot/verify
        _____________________
        handle requesting forgot password by inputting otp id and otp code and
        new password
    """

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            reset_password(**request.data)
        return Response(status=HTTP_204_NO_CONTENT)

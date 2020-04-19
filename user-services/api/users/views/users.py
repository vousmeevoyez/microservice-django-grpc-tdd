"""
    User Views
"""
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.response import Response

from api.users.serializers import (UserRegistrationSerializer, UserSerializer,
                                   VerifyUserSerializer)
from api.users.services.users import create_user, verify_user


class RegisterUserView(APIView):

    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user, otp_id = create_user(**serializer.data)
            serializer = UserSerializer(user)
            # add otp id in response body
            otp_response = {"otp": {"id": otp_id}}
            response = {**serializer.data, **otp_response}
            return Response(response)


class VerifyUserView(APIView):

    def post(self, request):
        serializer = VerifyUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            verify_user(**serializer.data)
            return Response(status=HTTP_204_NO_CONTENT)

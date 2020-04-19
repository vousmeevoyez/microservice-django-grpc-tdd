"""
    User Views
"""
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.response import Response

from api.users.serializers import (UserLoginSerializer)
from api.users.services.auth import login, logout


class LoginView(APIView):

    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            response = login(**serializer.data)
            return Response(response)


class LogoutView(APIView):

    def post(self, request):
        response = logout(request.user.id)
        return Response(response, status=HTTP_204_NO_CONTENT)

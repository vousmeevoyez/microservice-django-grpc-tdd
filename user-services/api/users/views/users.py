"""
    User Views
"""
from rest_framework.status import HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import RetrieveUpdateDestroyAPIView

from api.users.serializers import (
    UserRegistrationSerializer,
    UserSerializer,
    VerifyUserSerializer,
    ProfileSerializer,
    UpdatePasswordSerializer,
    UpdateMsisdnSerializer,
)
from api.users.models import Profile
from api.users.services.users import (
    create_user,
    verify_user,
    update_user_password,
    update_phone_no,
)
from api.utils.reusable.serializers import UserOwnViewSet


class RegisterUserView(APIView):
    """
        POST /user/registration
        __________________________
        Handle registering user
    """

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
    """
        POST /user/verify
        __________________________
        Handle verify user registration
    """

    def post(self, request):
        serializer = VerifyUserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            verify_user(**serializer.data)
            return Response(status=HTTP_204_NO_CONTENT)


class UserProfileView(RetrieveUpdateDestroyAPIView):
    """
        GET PUT PATCH /user/profile
        __________________________
        Handle fetch and update user profile
    """

    queryset = Profile.objects.all()
    serializer_class = UserSerializer

    def get_object(self):
        """ we just return the user so it can be deserialized by
        serializer_class that we set """
        return self.request.user

    def get_serializer_class(self):
        """ override default behaviour because serializer that used for request
        and response is different """
        serializer_class = UserSerializer
        if self.request.method in ["PUT", "PATCH"]:
            serializer_class = ProfileSerializer
        return serializer_class

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.request.user.profile
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, "_prefetched_objects_cache", None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)


class UpdatePasswordView(APIView):
    """
        PUT /user/profile/password
        __________________________
        Handle Update user password
    """

    def put(self, request):
        serializer = UpdatePasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            update_user_password(self.request.user, serializer.data["new_password"])
            return Response(status=HTTP_204_NO_CONTENT)


class UpdatePhoneView(APIView):
    """
        PUT /user/profile/phone
        __________________________
        Handle Update user phone ext + phone no
    """

    def put(self, request):
        serializer = UpdateMsisdnSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            update_phone_no(self.request.user, **serializer.data)
            return Response(status=HTTP_204_NO_CONTENT)

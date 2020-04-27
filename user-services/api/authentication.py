"""
    Custom Authentication Classes for DRF
"""
from django.contrib.auth import get_user_model
from rest_framework.authentication import RemoteUserAuthentication
from api.users.exceptions import UserNotFoundException

User = get_user_model()


class KongAuthentication:
    """
        Override default drf remote authentication, so if
        upstream header is detected automatically authenticate using user id
    """

    header = "HTTP_X_CONSUMER_CUSTOM_ID"

    def authenticate(self, request):
        user_id = request.META.get(self.header)
        if "headers" in request.META:
            user_id = request.META["headers"].get(self.header)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            print("usernotexist")
            return (None, None)

        if user and user.is_active:
            return (user, None)

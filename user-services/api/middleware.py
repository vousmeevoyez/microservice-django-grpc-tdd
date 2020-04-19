from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.middleware import RemoteUserMiddleware
from django.core.exceptions import ImproperlyConfigured

from api.users.exceptions import UserNotFoundException

User = get_user_model()


class KongGatewayHeaderMiddleware(RemoteUserMiddleware):
    # X-Consumer-Username
    header = 'HTTP_X_CONSUMER_CUSTOM_ID'

    def process_request(self, request):
        # AuthenticationMiddleware is required so that request.user exists.
        if not hasattr(request, 'user'):
            raise ImproperlyConfigured(
                "The Django remote user auth middleware requires the"
                " authentication middleware to be installed.  Edit your"
                " MIDDLEWARE setting to insert"
                " 'django.contrib.auth.middleware.AuthenticationMiddleware'"
                " before the RemoteUserMiddleware class.")
        try:
            user_id = request.META["headers"][self.header]
        except KeyError:
            # If specified header doesn't exist then remove any existing
            # authenticated remote-user, or return (leaving request.user set to
            # AnonymousUser by the AuthenticationMiddleware).
            if self.force_logout_if_no_header and request.user.is_authenticated:
                self._remove_invalid_user(request)
            return

        # look user by his user id
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raise UserNotFoundException
        else:
            request.user = user

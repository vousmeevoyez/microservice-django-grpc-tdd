"""
    User Urls
    ________________
"""
from django.urls import path
from rest_framework.routers import Route, SimpleRouter

from api.users.views import *

# router = SimpleRouter()
# router.register(r"profile", ProfileViewSet)

urlpatterns = [
    path("registration", RegisterUserView.as_view(), name="user-registration"),
    path("verify", VerifyUserView.as_view(), name="user-verification"),
    path("profile", UserProfileView.as_view(), name="user-profile"),
    path("profile/password", UpdatePasswordView.as_view(), name="user-password"),
    path("profile/phone", UpdatePhoneView.as_view(), name="user-phone"),
]
# urlpatterns += router.urls

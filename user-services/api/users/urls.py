from django.urls import path

from api.users.views import *

urlpatterns = [
    path("registration", RegisterUserView.as_view(), name="user-registration"),
    path("verify", VerifyUserView.as_view(), name="user-verification")
]

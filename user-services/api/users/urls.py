from django.urls import path

from api.users.views import *

urlpatterns = [
    path("registration", RegisterUserView.as_view(), name="user-registration"),
    path("verify", VerifyUserView.as_view(), name="user-verification"),
    path("otp/resend/<uuid:user_id>/",
         ResendOTPView.as_view(),
         name="user-otp-resend"),
    path("login", LoginView.as_view(), name="user-login"),
    path("logout", LogoutView.as_view(), name="user-logout")
]

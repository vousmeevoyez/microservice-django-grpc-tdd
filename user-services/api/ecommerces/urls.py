from django.urls import path
from rest_framework.routers import Route, SimpleRouter

from api.ecommerces.views import (PlatformViewSet)

router = SimpleRouter()
router.register(r"platforms", PlatformViewSet)

urlpatterns = [
    #    path("login", LoginView.as_view(), name="auth-login"),
    #    path("logout", LogoutView.as_view(), name="auth-logout"),
    #    path("forgot/request/<uuid:user_id>",
    #         RequestForgotPasswordView.as_view(),
    #         name="forgot-password"),
    #    path("forgot/verify",
    #         VerifyForgotPasswordView.as_view(),
    #         name="verify-password"),
    #    path("otp/resend/<uuid:user_id>",
    #         ResendOTPView.as_view(),
    #         name="otp-resend"),
]
urlpatterns += router.urls

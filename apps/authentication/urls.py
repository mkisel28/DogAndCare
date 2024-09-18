from django.urls import path

from apps.api.v1.authentication.views.views import (
    APILogoutView,
    CustomVerifyEmailView,
    EmailAuthRequestView,
)
from dj_rest_auth.app_settings import api_settings



urlpatterns = [
    path("", EmailAuthRequestView.as_view(), name="auth"),
    path(
        "verify/",
        CustomVerifyEmailView.as_view(),
        name="auth-verify",
    ),
    path("logout/", APILogoutView.as_view(), name="rest_logout"),
]


if api_settings.USE_JWT:
    from rest_framework_simplejwt.views import TokenVerifyView

    from dj_rest_auth.jwt_auth import get_refresh_view

    urlpatterns += [
        path("token/verify/", TokenVerifyView.as_view(), name="token_verify"),
        path("token/refresh/", get_refresh_view().as_view(), name="token_refresh"),
    ]

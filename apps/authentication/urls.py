from django.urls import path, include
from dj_rest_auth.app_settings import api_settings
from rest_framework.routers import DefaultRouter
from apps.api.v1.authentication.views.views import (
    APILogoutView,
    CustomTokenRefreshView,
    CustomTokenVerifyView,
    CustomVerifyEmailView,
    EmailAuthRequestView,
)


router = DefaultRouter()
router.register(r"", EmailAuthRequestView, basename="auth")


urlpatterns = [
    path(
        "verify/",
        CustomVerifyEmailView.as_view(),
        name="auth-verify",
    ),
    path("", include(router.urls)),
    path("logout/", APILogoutView.as_view(), name="rest_logout"),
]


if api_settings.USE_JWT:

    urlpatterns += [
        path("token/refresh/", CustomTokenRefreshView.as_view(), name="token_refresh"),
        path("token/verify/", CustomTokenVerifyView.as_view(), name="token_verify"),
    ]

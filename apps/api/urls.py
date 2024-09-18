from django.urls import path
from django.urls.conf import include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from apps.api.v1.authentication.views.views import (
    EmailAuthRequestView,
    CustomRegisterView,
    CustomVerifyEmailView,
)
from dj_rest_auth.registration.views import RegisterView

urlpatterns = [
    path("v1/", include("apps.api.v1.urls")),
    path("auth/", include("apps.authentication.urls")),

    path("schema-yaml/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]


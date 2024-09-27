from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from apps.api.v1.authentication.views.views import GoogleLogin


urlpatterns = [
    path("v1/", include("apps.api.v1.urls")),
    path("auth/", include("apps.authentication.urls")),
    path("user/", include("apps.api.v1.users.urls")),
    path("pets/", include("apps.api.v1.pets.urls")),
    path("reminders/", include("apps.api.v1.reminders.urls")),
    path("accounts/", include("allauth.urls")),
    path("auth/social/google/", GoogleLogin.as_view(), name="google_login"),
    path("schema-yaml/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

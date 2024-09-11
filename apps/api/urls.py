from django.urls import path
from django.urls.conf import include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

urlpatterns = [
    path("v1/", include("apps.api.v1.urls")),
    path("auth/", include("dj_rest_auth.urls")),
    path(
        "auth/registration/", include("dj_rest_auth.registration.urls")
    ),
    path("schema-yaml/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "swagger/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"
    ),
    path("redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]


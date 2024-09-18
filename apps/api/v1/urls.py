from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from apps.api.v1.authentication.views.views import EmailAuthRequestView

app_name = "api_v1"

router = routers.DefaultRouter()
urlpatterns = [
    path("", include(router.urls)),
]

from django.urls import path, include
from rest_framework import routers


app_name = "api_v1"

router = routers.DefaultRouter()
urlpatterns = [
    path("", include(router.urls)),
]

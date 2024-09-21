from django.urls import path, include


from apps.api.v1.pets.views.views import PetViewSet
from apps.api.v1.users.views.views import (
    CurrentUserView,
)

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"pets", PetViewSet, basename="pets")

urlpatterns = [
    path("", CurrentUserView.as_view(), name="user"),
    path("", include(router.urls)),
]

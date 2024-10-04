from django.urls import path, include


from apps.api.v1.pets.views.views import PetViewSet, SymptomLogViewSet
from apps.api.v1.users.views.views import (
    CurrentUserView,
)

from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework_nested import routers

router = SimpleRouter()
router.register(r"pets", PetViewSet, basename="pets")

pets_router = routers.NestedSimpleRouter(router, r"pets", lookup="pet")
pets_router.register(r"symptoms", SymptomLogViewSet, basename="symptom-logs")

urlpatterns = [
    path("", CurrentUserView.as_view(), name="user"),
    path("", include(router.urls)),
    path("", include(pets_router.urls)),
]

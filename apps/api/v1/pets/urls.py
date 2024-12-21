from django.urls import include, path
from rest_framework.routers import DefaultRouter

from apps.api.v1.pets.views.views import BreedViewSet, TemperamentViewSet

router = DefaultRouter()
router.register(r"breeds", BreedViewSet, basename="breed")
router.register(r"temperaments", TemperamentViewSet, basename="temperament")


urlpatterns = [
    path("", include(router.urls)),
]

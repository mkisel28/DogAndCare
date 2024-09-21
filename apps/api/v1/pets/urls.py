from django.urls import path, include

from apps.api.v1.pets.views.views import BreedViewSet, TemperamentViewSet

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"breeds", BreedViewSet, basename="breed")
router.register(r"temperaments", TemperamentViewSet, basename="temperament")


urlpatterns = [
    path("", include(router.urls)),
]

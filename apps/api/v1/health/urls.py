from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import views

router = DefaultRouter()

router.register(
    r"symptom-categories",
    views.SymptomCategoryViewSet,
    basename="symptomcategory",
)
router.register(r"symptoms", views.SymptomViewSet, basename="symptom")


urlpatterns = [
    path("", include(router.urls)),
]

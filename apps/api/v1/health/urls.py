from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .views import views


router = DefaultRouter()
router.register(
    r"symptom-categories", views.SymptomCategoryViewSet, basename="symptomcategory"
)
router.register(r"symptoms", views.SymptomViewSet, basename="symptom")
# router.register(r'daily-logs', views.DailyLogViewSet, basename='dailylog')


urlpatterns = [
    path("", include(router.urls)),
]
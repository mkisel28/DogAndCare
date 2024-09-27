from rest_framework.routers import DefaultRouter

from apps.api.v1.reminders.views.views import ReminderViewSet

router = DefaultRouter()
router.register(r"", ReminderViewSet, basename="reminder")

urlpatterns = router.urls

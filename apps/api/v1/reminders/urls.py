from rest_framework.routers import DefaultRouter

from apps.api.v1.reminders.views.views import ReminderCategoryViewSet

router = DefaultRouter()
router.register(r"categories", ReminderCategoryViewSet, basename="reminder_category")

urlpatterns = router.urls

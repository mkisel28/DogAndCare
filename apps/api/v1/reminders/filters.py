from django.db.models import Q
from django_filters import rest_framework as filters

from apps.reminders.models import Reminder, ReminderType


class ReminderFilter(filters.FilterSet):
    search = filters.CharFilter(method="filter_search")

    time_from = filters.DateTimeFilter(
        field_name="reminder_time",
        lookup_expr="gte",
        input_formats=["%Y-%m-%dT%H:%M:%SZ"],
        help_text="Start date for reminder time (UTC, format: YYYY-MM-DDTHH:MM:SSZ)",
    )
    time_to = filters.DateTimeFilter(
        field_name="reminder_time",
        lookup_expr="lte",
        input_formats=["%Y-%m-%dT%H:%M:%SZ"],
        help_text="End date for reminder time (UTC, format: YYYY-MM-DDTHH:MM:SSZ)",
    )
    reminder_type = filters.ModelChoiceFilter(
        queryset=ReminderType.objects.all(),
        field_name="reminder_type",
        help_text="Filter by reminder type",
    )
    is_recurring = filters.BooleanFilter(
        field_name="is_recurring", help_text="Filter by recurring status"
    )
    created_after = filters.DateTimeFilter(
        field_name="created_at",
        lookup_expr="gte",
        input_formats=["%Y-%m-%dT%H:%M:%SZ"],
        help_text="Filter reminders created after this date (UTC)",
    )
    ordering = filters.OrderingFilter(
        fields=(
            ("created_at", "created_at"),
            ("reminder_time", "reminder_time"),
            ("title", "title"),
        ),
        field_labels={
            "created_at": "Creation Date",
            "reminder_time": "Reminder Time",
            "title": "Title",
        },
        help_text="Sort by: created_at, -created_at, reminder_time, -reminder_time, title, -title",
    )

    class Meta:
        model = Reminder
        fields = [
            "search",
            "time_from",
            "time_to",
            "reminder_type",
            "is_recurring",
            "created_after",
            "ordering",
        ]

    def filter_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value) | Q(description__icontains=value)
        )

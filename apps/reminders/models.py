from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

from apps.pets.models import Pet


class Reminder(models.Model):
    title = models.CharField(max_length=255, help_text="Title of the reminder")
    description = models.TextField(
        null=True, blank=True, help_text="Description of the reminder"
    )
    reminder_type = models.CharField(
        max_length=255, help_text="Type of reminder", blank=True, null=True
    )
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="When the reminder was created"
    )
    reminder_time = models.DateTimeField(help_text="When the reminder should notify")
    is_recurring = models.BooleanField(
        default=False, help_text="Is this a recurring reminder?"
    )
    frequency_in_minutes = models.PositiveIntegerField(
        null=True, blank=True, help_text="Frequency of recurring reminder in minutes"
    )
    # Связь M2M с собакой
    pets = models.ManyToManyField(
        Pet, related_name="reminders", help_text="Related pets for the reminder"
    )

    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="reminders",
        help_text="Owner of the reminder",
    )

    class Meta:
        ordering = ["-reminder_time"]
        verbose_name = "Reminder"
        verbose_name_plural = "Reminders"

    def __str__(self):
        return self.title

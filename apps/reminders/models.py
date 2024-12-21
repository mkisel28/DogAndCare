from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver

from apps.pets.models import Pet


class ReminderCategory(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
        help_text="Category of reminder",
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Description of the reminder type",
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Is this category active?",
    )

    def __str__(self):
        return self.name


class ReminderType(models.Model):
    category = models.ForeignKey(
        ReminderCategory,
        on_delete=models.CASCADE,
        related_name="types",
        help_text="Category to which this type belongs",
    )
    name = models.CharField(max_length=255, unique=True, help_text="Type of reminder")
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Description of the reminder type",
    )
    is_active = models.BooleanField(default=True, help_text="Is this category active?")

    def __str__(self):
        return f"{self.category.name}: {self.name}"


class Reminder(models.Model):
    title = models.CharField(max_length=255, help_text="Title of the reminder")
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Description of the reminder",
    )
    reminder_type = models.ForeignKey(
        ReminderType,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="reminders",
        help_text="Type of reminder",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="When the reminder was created",
    )
    reminder_time = models.DateTimeField(help_text="When the reminder should notify")
    is_recurring = models.BooleanField(
        default=False,
        help_text="Is this a recurring reminder?",
    )
    frequency_in_minutes = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Frequency of recurring reminder in minutes",
    )
    # Связь M2M с собакой
    pets = models.ManyToManyField(
        Pet,
        related_name="reminders",
        help_text="Related pets for the reminder",
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


@receiver(post_migrate)
def create_default_reminder_types(sender, **kwargs):
    from django.db.utils import IntegrityError

    if sender.name == "apps.reminders":
        categories = {
            "Wellness": [
                "Wellness Exams",
                "Preventive Care",
                "Grooming",
                "Boarding",
            ],
            "Appointments": [
                "Consultation",
            ],
            "Medicine": [
                "Vaccination",
                "Dental Service",
                "Spraying/Neutering",
                "Diagnostic Tests",
                "X-ray and Imaging",
                "Surgery",
                "Emergency Care",
                "Microchipping",
            ],
        }

        for category_name, types in categories.items():
            category, created = ReminderCategory.objects.get_or_create(
                name=category_name,
            )
            for type_name in types:
                try:
                    ReminderType.objects.get_or_create(
                        name=type_name,
                        category=category,
                    )
                except IntegrityError:
                    pass

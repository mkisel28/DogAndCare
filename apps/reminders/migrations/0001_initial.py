import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("pets", "0004_remove_pet_birth_day_remove_pet_birth_month_and_more"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Reminder",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "title",
                    models.CharField(help_text="Title of the reminder", max_length=255),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="Description of the reminder", null=True
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="When the reminder was created"
                    ),
                ),
                (
                    "reminder_time",
                    models.DateTimeField(help_text="When the reminder should notify"),
                ),
                (
                    "is_recurring",
                    models.BooleanField(
                        default=False, help_text="Is this a recurring reminder?"
                    ),
                ),
                (
                    "frequency_in_minutes",
                    models.PositiveIntegerField(
                        blank=True,
                        help_text="Frequency of recurring reminder in minutes",
                        null=True,
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        help_text="Owner of the reminder",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="reminders",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "pets",
                    models.ManyToManyField(
                        help_text="Related pets for the reminder",
                        related_name="reminders",
                        to="pets.pet",
                    ),
                ),
            ],
            options={
                "verbose_name": "Reminder",
                "verbose_name_plural": "Reminders",
                "ordering": ["-reminder_time"],
            },
        ),
    ]

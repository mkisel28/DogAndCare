# Generated by Django 5.1.1 on 2024-12-21 13:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("reminders", "0002_reminder_reminder_type"),
    ]

    operations = [
        migrations.CreateModel(
            name="ReminderCategory",
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
                    "name",
                    models.CharField(
                        help_text="Category of reminder",
                        max_length=255,
                        unique=True,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Description of the reminder type",
                        null=True,
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Is this category active?",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ReminderType",
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
                    "name",
                    models.CharField(
                        help_text="Type of reminder",
                        max_length=255,
                        unique=True,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="Description of the reminder type",
                        null=True,
                    ),
                ),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Is this category active?",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        help_text="Category to which this type belongs",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="types",
                        to="reminders.remindercategory",
                    ),
                ),
            ],
        ),
        migrations.AlterField(
            model_name="reminder",
            name="reminder_type",
            field=models.ForeignKey(
                blank=True,
                help_text="Type of reminder",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="reminders",
                to="reminders.remindertype",
            ),
        ),
    ]

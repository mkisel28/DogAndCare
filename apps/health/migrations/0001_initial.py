# Generated by Django 5.1.1 on 2024-10-03 15:53

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("pets", "0004_remove_pet_birth_day_remove_pet_birth_month_and_more"),
    ]

    operations = [
        migrations.CreateModel(
            name="SymptomCategory",
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
                        help_text="Название категории симптомов",
                        max_length=50,
                        unique=True,
                    ),
                ),
                (
                    "description",
                    models.TextField(
                        blank=True, help_text="Описание категории", null=True
                    ),
                ),
            ],
            options={
                "verbose_name": "Категория симптома",
                "verbose_name_plural": "Категории симптомов",
            },
        ),
        migrations.CreateModel(
            name="Symptom",
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
                        help_text="Название симптома", max_length=100, unique=True
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        help_text="Категория симптома",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="symptoms",
                        to="health.symptomcategory",
                    ),
                ),
            ],
            options={
                "verbose_name": "Симптом",
                "verbose_name_plural": "Симптомы",
                "ordering": ["category__name", "name"],
            },
        ),
        migrations.CreateModel(
            name="DailyLog",
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
                    "date",
                    models.DateField(
                        default=django.utils.timezone.now, help_text="Дата лога"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, help_text="Дата и время создания записи"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="Дата и время последнего обновления записи",
                    ),
                ),
                (
                    "pet",
                    models.ForeignKey(
                        help_text="Питомец",
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="daily_logs",
                        to="pets.pet",
                    ),
                ),
                (
                    "symptoms",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Симптомы",
                        related_name="daily_logs",
                        to="health.symptom",
                    ),
                ),
            ],
            options={
                "verbose_name": "Ежедневный лог",
                "verbose_name_plural": "Ежедневные логи",
                "ordering": ["-date"],
                "unique_together": {("pet", "date")},
            },
        ),
    ]
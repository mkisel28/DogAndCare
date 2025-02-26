import uuid
from django.db import models


class Multimedia(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    url = models.URLField(
        max_length=2048,
        help_text="URL изображения",
        verbose_name="URL изображения",
    )
    type = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        help_text="Тип изображения",
        verbose_name="Тип",
    )
    description = models.TextField(
        null=True,
        blank=True,
        help_text="Описание изображения",
        verbose_name="Описание",
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        help_text="Дата создания",
        verbose_name="Дата создания",
    )

    class Meta:
        indexes = [
            models.Index(fields=["type"]),
        ]
        verbose_name = "Мультимедиа"
        verbose_name_plural = "Мультимедиа"

    def __str__(self):
        return self.url

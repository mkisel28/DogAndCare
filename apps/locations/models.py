from django.db import models


class Country(models.Model):
    name = models.CharField(
        max_length=255, help_text="Наименование страны", verbose_name="Страна"
    )
    code = models.CharField(max_length=10, help_text="Код страны", verbose_name="Код")

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
            models.Index(fields=["code"]),
        ]
        verbose_name = "Страна"
        verbose_name_plural = "Страны"

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(
        max_length=255, help_text="Наименование города", verbose_name="Город"
    )
    country = models.ForeignKey(
        Country,
        on_delete=models.CASCADE,
        related_name="cities",
        help_text="Страна",
        verbose_name="Страна",
    )

    class Meta:
        indexes = [
            models.Index(fields=["name"]),
        ]
        verbose_name = "Город"
        verbose_name_plural = "Города"

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(
        max_length=255, help_text="Наименование языка", verbose_name="Язык"
    )
    code = models.CharField(max_length=10, help_text="Код языка", verbose_name="Код")

    class Meta:
        verbose_name = "Язык"
        verbose_name_plural = "Языки"

    def __str__(self):
        return self.name

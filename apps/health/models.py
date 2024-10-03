from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from apps.pets.models import Pet


class SymptomCategory(models.Model):
    name = models.CharField(
        max_length=50, unique=True, help_text="Название категории симптомов"
    )
    description = models.TextField(
        blank=True, null=True, help_text="Описание категории"
    )

    class Meta:
        verbose_name = "Категория симптома"
        verbose_name_plural = "Категории симптомов"

    def __str__(self):
        return self.name


class Symptom(models.Model):
    category = models.ForeignKey(
        SymptomCategory,
        on_delete=models.CASCADE,
        related_name="symptoms",
        help_text="Категория симптома",
    )
    name = models.CharField(max_length=100, unique=True, help_text="Название симптома")

    class Meta:
        verbose_name = "Симптом"
        verbose_name_plural = "Симптомы"
        ordering = ["category__name", "name"]
        unique_together = ("name", "category")

    def __str__(self):
        return f"{self.name} ({self.category.name})"


class DailyLog(models.Model):
    pet = models.ForeignKey(
        Pet, on_delete=models.CASCADE, related_name="daily_logs", help_text="Питомец"
    )
    date = models.DateField(default=timezone.now, help_text="Дата лога")
    symptoms = models.ManyToManyField(
        Symptom, blank=True, related_name="daily_logs", help_text="Симптомы"
    )

    created_at = models.DateTimeField(
        auto_now_add=True, help_text="Дата и время создания записи"
    )
    updated_at = models.DateTimeField(
        auto_now=True, help_text="Дата и время последнего обновления записи"
    )

    class Meta:
        verbose_name = "Ежедневный лог"
        verbose_name_plural = "Ежедневные логи"
        unique_together = ("pet", "date")
        ordering = ["-date"]

    def __str__(self):
        return f"{self.pet.name} - {self.date}"

    def clean(self):
        if self.date > timezone.now().date():
            raise ValidationError("Дата не может быть в будущем.")

    def add_symptoms(self, symptom_ids):
        """Добавить симптомы к логу"""
        symptoms = Symptom.objects.filter(id__in=symptom_ids)
        self.symptoms.add(*symptoms)

    def remove_symptoms(self, symptom_ids):
        """Удалить симптомы из лога"""
        symptoms = Symptom.objects.filter(id__in=symptom_ids)
        self.symptoms.remove(*symptoms)

    @classmethod
    def get_today_log(cls, pet):
        """Получить или создать лог для сегодня"""
        today = timezone.now().date()
        if isinstance(pet, int):
            pet = Pet.objects.filter(id=pet).first()
            print(pet)
            print(pet)
            print(pet)
            if not pet:
                raise ValidationError("Питомец не найден.")
        log, created = cls.objects.get_or_create(pet=pet, date=today)
        return log


@receiver(post_migrate)
def create_default_symptoms(sender, **kwargs):
    from django.db.utils import IntegrityError

    if sender.name == "apps.health":
        categories = {
            "Mood": [
                "Happy",
                "Neutral",
                "Playful",
                "Sad",
                "Tired",
                "Sleeping all day",
                "Restless",
                "Aggressive",
            ],
            "Overall Well-Being": [
                "All good",
                "Excited",
                "Excessive drooling",
                "Vomiting",
                "Diarrhea",
                "In pain",
                "Loss of appetite",
                "Heavy, rapid breathing",
                "Change in urine or stool",
                "Frequent urination",
                "Other behavior changes",
                "Dry nose",
            ],
            "Feeding": [
                "Today's meal: All eaten",
                "Didn't finish",
                "Refused to eat",
                "Spoiled with treats",
                "Ate something forbidden",
                "Ate something unknown",
                "Overate",
                "New food/New diet",
            ],
            "Physical Activity": [
                "Walk",
                "Running",
                "Active outdoor play",
                "Indoor play",
                "Mental games",
                "Swimming",
                "Command/Trick practice",
                "Agility training",
            ],
            "Digestion and Stool": [
                "Vomiting",
                "Bloating",
                "Constipation",
                "Diarrhea",
                "Blood in stool",
                "Mucus in stool",
                "Chewed grass/bark",
                "Chewed furniture or objects",
            ],
            "Unusual Events": [
                "Met a new friend (dog, cat, or human)",
                "Traveled by transport",
                "Vet visit",
                "Grooming salon visit",
                "Ran away",
                "Home alone (for a long time)",
                "Fought with another dog",
                "Frightened",
                "Separation from owner",
                "Loss of owner",
            ],
        }

        for category_name, symptoms in categories.items():
            category, created = SymptomCategory.objects.get_or_create(
                name=category_name
            )
            for symptom_name in symptoms:
                try:
                    Symptom.objects.get_or_create(name=symptom_name, category=category)
                except IntegrityError:
                    pass

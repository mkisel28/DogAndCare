from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models

from apps.pets.models import Pet


class Walk(models.Model):
    pet = models.ForeignKey(
        Pet,
        on_delete=models.CASCADE,
        related_name="walks",
        help_text="The pet being walked",
    )
    owner = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="walks",
        help_text="The owner of the walk",
    )
    start_time = models.DateTimeField(help_text="The start time of the walk")
    end_time = models.DateTimeField(
        null=True,
        blank=True,
        help_text="The end time of the walk",
    )
    duration = models.PositiveIntegerField(
        null=True,
        blank=True,
        help_text="Duration of the walk in minutes",
    )

    def save(self, *args, **kwargs):
        if self.start_time and self.end_time:
            self.duration = int((self.end_time - self.start_time).total_seconds() / 60)
        super().save(*args, **kwargs)

        if self.duration:
            date = self.start_time.date()
            walk_stats, created = WalkStats.objects.get_or_create(
                pet=self.pet,
                date=date,
            )
            walk_stats.increment_walk(self.duration)

    def clean(self):
        if self.start_time and self.end_time and self.start_time > self.end_time:
            raise ValidationError("End time must be after start time")

    def __str__(self):
        return f"Walk for {self.pet.name} on {self.start_time.date()}"


class WalkStats(models.Model):
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="walk_stats")
    date = models.DateField(help_text="The date of the aggregated walks")
    total_duration = models.PositiveIntegerField(
        help_text="Total duration of walks in minutes",
        default=0,
    )
    total_walks = models.PositiveIntegerField(
        help_text="Total number of walks",
        default=0,
    )

    class Meta:
        unique_together = ("pet", "date")

    def increment_walk(self, duration):
        self.total_duration += duration
        self.total_walks += 1
        self.save()

    @staticmethod
    def get_weekly_stats(pet_id, start_date, end_date):
        stats = WalkStats.objects.filter(
            pet__id=pet_id,
            date__range=(start_date, end_date),
        )
        total_duration = sum(stat.total_duration for stat in stats)
        total_walks = sum(stat.total_walks for stat in stats)
        return {
            "start_date": start_date,
            "end_date": end_date,
            "total_walks": total_walks,
            "total_duration_minutes": total_duration,
        }

    @staticmethod
    def get_stat_day_by_day(pet_id, start_date, end_date):
        stats = WalkStats.objects.filter(
            pet__id=pet_id,
            date__range=(start_date, end_date),
        ).order_by("-date")
        return stats

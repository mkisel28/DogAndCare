from rest_framework import serializers
from apps.pets.models import Pet
from apps.reminders.models import Reminder
from django.utils import timezone


class PetDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ["id", "name", "avatar"]


class ReminderSerializer(serializers.ModelSerializer):
    pet_ids = serializers.PrimaryKeyRelatedField(
        queryset=Pet.objects.all(),
        many=True,
        help_text="List of pets related to this reminder",
        write_only=True,
    )
    pets_details = PetDetailSerializer(
        source="pets",
        many=True,
        help_text="List of pets related to this reminder",
        read_only=True,
        required=False,
    )

    class Meta:
        model = Reminder
        fields = [
            "id",
            "title",
            "description",
            "reminder_type",
            "reminder_time",
            "is_recurring",
            "frequency_in_minutes",
            "pet_ids",
            "pets_details",
        ]

    def validate_pets(self, value):
        user = self.context["request"].user
        for pet in value:
            if pet.owner != user:
                raise serializers.ValidationError(
                    f"Pet does not belong to you.", code="invalid_pet_owner"
                )
        return value

    def validate_reminder_time(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                "The reminder time cannot be in the past.", code="invalid_reminder_time"
            )
        return value

    def validate_frequency_in_minutes(self, value):
        if self.initial_data.get("is_recurring", None) and not value:
            raise serializers.ValidationError(
                "This field is required for recurring reminders.",
                code="required_for_recurring",
            )
        return value

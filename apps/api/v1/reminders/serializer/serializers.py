from django.utils import timezone
from rest_framework import serializers

from apps.pets.models import Pet
from apps.reminders.models import Reminder, ReminderCategory, ReminderType


class PetDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = ["id", "name", "avatar"]


class ReminderTypeSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source="category.name", read_only=True)

    class Meta:
        model = ReminderType
        fields = ["id", "name", "description", "category_name"]


class ReminderCategorySerializer(serializers.ModelSerializer):
    reminder_types = ReminderTypeSerializer(
        source="types",
        many=True,
        read_only=True,
        help_text="List of reminder types related to this category",
    )

    class Meta:
        model = ReminderCategory
        fields = ["id", "name", "description", "reminder_types"]


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
    reminder_type = ReminderTypeSerializer(
        read_only=True,
        help_text="Details of the reminder type",
    )
    reminder_type_id = serializers.PrimaryKeyRelatedField(
        queryset=ReminderType.objects.all(),
        source="reminder_type",
        write_only=True,
        help_text="ID of the reminder type",
        allow_null=True,
    )

    class Meta:
        model = Reminder
        fields = [
            "id",
            "title",
            "description",
            "reminder_type",
            "reminder_type_id",
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
                    "Pet does not belong to you.",
                    code="invalid_pet_owner",
                )
        return value

    def validate_reminder_time(self, value):
        if value < timezone.now():
            raise serializers.ValidationError(
                "The reminder time cannot be in the past.",
                code="invalid_reminder_time",
            )
        return value

    def validate_frequency_in_minutes(self, value):
        if self.initial_data.get("is_recurring", None) and not value:
            raise serializers.ValidationError(
                "This field is required for recurring reminders.",
                code="required_for_recurring",
            )
        return value

    def create(self, validated_data):
        pet_ids = validated_data.pop("pet_ids", [])
        reminder = Reminder.objects.create(**validated_data)

        reminder.pets.set(pet_ids)
        return reminder

    def update(self, instance, validated_data):
        pet_ids = validated_data.pop("pet_ids", None)
        if pet_ids is not None:
            instance.pets.set(pet_ids)

        return super().update(instance, validated_data)

from datetime import date, timedelta

from rest_framework import serializers

from apps.pets.models import Breed, Pet, Temperament


class CreatePetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pet
        fields = "__all__"


class BreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Breed
        fields = ["id", "name"]


class TemperamentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Temperament
        fields = "__all__"


class PetSerializer(serializers.ModelSerializer):
    breed = serializers.CharField(source="breed.name", required=False, read_only=True)
    breed_id = serializers.PrimaryKeyRelatedField(
        queryset=Breed.objects.all(),
        source="breed",
        write_only=True,
        required=False,
    )

    class Meta:
        model = Pet
        fields = [
            "id",
            "name",
            "avatar",
            "breed",
            "breed_id",
            "birth_date",
            "sex",
            "is_neutered",
            "weight",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["created_at", "updated_at"]

    def validate_birth_date(self, value):
        today = date.today()

        if value > today:
            raise serializers.ValidationError(
                "The birth date cannot be in the future.",
                code="future_birth_date",
            )

        max_age = today - timedelta(days=50 * 365)
        if value < max_age:
            raise serializers.ValidationError(
                "The pet can not be older than 50 years.",
                code="max_age_exceeded",
            )
        return value

    def create(self, validated_data):
        user = self.context["request"].user
        validated_data["owner"] = user
        return super().create(validated_data)

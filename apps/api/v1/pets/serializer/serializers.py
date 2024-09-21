from rest_framework import serializers

from apps.pets.models import Breed, Pet, Temperament


class PetsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    breed = serializers.CharField(source="breed.name", required=False)
    temperament = serializers.SlugRelatedField(
        many=True, read_only=True, slug_field="name"
    )
    birth = serializers.SerializerMethodField()

    class Meta:
        model = Pet
        fields = [
            "id",
            "name",
            "owner",
            "breed",
            "birth",
            "sex",
            "temperament",
            "is_neutered",
            "weight",
            "created_at",
            "updated_at",
        ]

    def get_birth(self, obj) -> str | None:
        date_of_birth = obj.get_date_of_birth()
        if date_of_birth:
            return date_of_birth.replace("-", ".")
        return None


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
    owner = serializers.ReadOnlyField(source="owner.username")
    breed = serializers.PrimaryKeyRelatedField(
        queryset=Breed.objects.all(), required=False
    )
    temperament = serializers.PrimaryKeyRelatedField(
        queryset=Temperament.objects.all(), many=True, required=False
    )

    class Meta:
        model = Pet
        fields = "__all__"

    def create(self, validated_data):
        temperament_data = validated_data.pop("temperament", [])
        pet = Pet.objects.create(owner=self.context["request"].user, **validated_data)
        pet.temperament.set(temperament_data)  # Связь с темпераментами через M2M
        return pet

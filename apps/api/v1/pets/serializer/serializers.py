from rest_framework import serializers

from apps.pets.models import Breed, Pet, Temperament


class PetsSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    breed = serializers.CharField(source="breed.name", required=False)

    class Meta:
        model = Pet
        fields = [
            "id",
            "name",
            "owner",
            "breed",
            "birth_date",
            "sex",
            "is_neutered",
            "weight",
            "created_at",
            "updated_at",
        ]


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


class PetCreateSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source="owner.username")
    breed = serializers.PrimaryKeyRelatedField(
        queryset=Breed.objects.all(), required=False
    )

    class Meta:
        model = Pet
        fields = "__all__"

    def create(self, validated_data):
        pet = Pet.objects.create(owner=self.context["request"].user, **validated_data)
        return pet

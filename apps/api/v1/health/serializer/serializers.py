from rest_framework import serializers
from apps.health.models import DailyLog, Symptom, SymptomCategory
from apps.pets.models import Breed, Pet


from rest_framework import serializers
from django.contrib.auth.models import User


class SymptomCategorySerializer(serializers.ModelSerializer):
    symptoms = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = SymptomCategory
        fields = ["id", "name", "description", "symptoms"]


class SymptomSerializer(serializers.ModelSerializer):
    category = SymptomCategorySerializer(read_only=True)

    class Meta:
        model = Symptom
        fields = ["id", "name", "category"]


class SymptomRetrieveSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.name", read_only=True)
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=SymptomCategory.objects.all(), source="category", write_only=True
    )

    class Meta:
        model = Symptom
        fields = ["id", "name", "category", "category_id"]


class DailyLogSerializer(serializers.ModelSerializer):
    symptoms_id = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Symptom.objects.all(),
        required=False,
        write_only=True,
    )

    # pet_id = serializers.PrimaryKeyRelatedField(
    #     many=False, queryset=Pet.objects.all(), required=False, write_only=True
    # )
    pet = serializers.StringRelatedField(source="pet.name", read_only=True)
    symptoms = SymptomRetrieveSerializer(many=True, read_only=True)

    class Meta:
        model = DailyLog
        fields = [
            "id",
            "pet",
            # "pet_id",
            "date",
            "symptoms",
            "symptoms_id",
            "created_at",
            "updated_at",
        ]
        read_only_fields = ["date", "created_at", "updated_at"]

    def create(self, validated_data):
        pet = self.context.get("pet_id")
        if not pet:
            raise serializers.ValidationError("Питомец не указан.")
        log = DailyLog.get_today_log(pet)
        if "symptoms_id" in validated_data:
            log.symptoms.set(validated_data["symptoms_id"])
        log.save()
        return log

    def update(self, instance, validated_data):
        if "symptoms_id" in validated_data:
            instance.symptoms.set(validated_data["symptoms_id"])
        instance.save()
        return instance

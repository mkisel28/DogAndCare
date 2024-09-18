from rest_framework import serializers
from django.contrib.auth.models import User
from apps.users.models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["date_of_birth", "bio"]



class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(
        source="profile.avatar", read_only=False, required=False
    )

    date_of_birth = serializers.DateField(
        source="profile.date_of_birth", read_only=False, required=False
    )
    bio = serializers.CharField(
        source="profile.bio", max_length=500, read_only=False, required=False
    )
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "date_of_birth",
            "bio",
            "avatar",
        ]

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("profile", {})

        profile = instance.profile
        for attr, value in profile_data.items():
            setattr(profile, attr, value)
        profile.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        return instance

class TokensSerializer(serializers.Serializer):
    access = serializers.CharField()
    refresh = serializers.CharField()
class AuthUserSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    tokens = TokensSerializer()

    class Meta:
        model = User
        fields = ["user", "tokens"]


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=False, help_text="Refresh токен, который нужно деактивировать")
    all_tokens = serializers.BooleanField(required=False, help_text="Если true, будут деактивированы все refresh токены пользователя")

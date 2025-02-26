from allauth.socialaccount.models import SocialAccount
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=50, allow_blank=True)
    last_name = serializers.CharField(max_length=50, allow_blank=True)
    avatar_url = serializers.ImageField(
        source="profile.avatar",
        read_only=False,
        allow_empty_file=True,
        allow_null=True,
    )
    date_of_birth = serializers.DateField(
        source="profile.date_of_birth",
        read_only=False,
        allow_null=True,
    )
    bio = serializers.CharField(
        source="profile.bio",
        max_length=500,
        read_only=False,
        allow_blank=True,
        allow_null=True,
    )
    email = serializers.EmailField(read_only=True)

    social_accounts = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "email",
            "first_name",
            "last_name",
            "date_of_birth",
            "bio",
            "avatar_url",
            "social_accounts",
        ]

    @extend_schema_field(
        serializers.ListField(
            child=serializers.CharField(default="Google"),
        ),
    )
    def get_social_accounts(self, user):
        """Метод для получения информации о социальных аккаунтах пользователя."""
        connected_social_accounts = SocialAccount.objects.filter(user=user)
        if not connected_social_accounts:
            return []
        return [account.provider for account in connected_social_accounts]

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
    refresh_token = serializers.CharField(
        required=False,
        help_text="Refresh токен, который нужно деактивировать",
    )
    all_tokens = serializers.BooleanField(
        required=False,
        help_text="Если true, будут деактивированы все refresh токены пользователя",
    )

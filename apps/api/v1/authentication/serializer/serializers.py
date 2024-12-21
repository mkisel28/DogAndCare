import re

from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.serializers import (
    RegisterSerializer,
    SocialLoginSerializer,
)
from dj_rest_auth.serializers import LoginSerializer
from rest_framework import serializers


class CodeSerializer(serializers.Serializer):
    code = serializers.CharField(
        max_length=6,
        required=True,
        help_text="A 6-digit confirmation code sent to the user's email address.",
    )


class VerifyEmailCodeSerializer(serializers.Serializer):
    email = serializers.EmailField(
        required=True,
        help_text="The email address of the user to verify.",
    )
    code = serializers.CharField(
        max_length=6,
        required=True,
        help_text="A 6-digit confirmation code sent to the user's email address.",
    )


class CustomRegisterSerializer(RegisterSerializer):
    username = None
    password1 = None
    password2 = None

    def get_cleaned_data(self):
        return {
            "email": self.validated_data.get("email", ""),
        }

    def validate_password1(self, password):
        pass

    def validate(self, data):
        return data

    def validate_email(self, email):
        email = super().validate_email(email)
        regex = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"

        if not re.match(regex, email):
            raise serializers.ValidationError("Enter a valid email address.")
        return email

    def save(self, request):
        user = super().save(request)
        return user


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True)


class GoogleLoginSerializer(SocialLoginSerializer):
    access_token = serializers.CharField()
    code = None

    class Meta:
        fields = ("access_token",)

    def validate(self, attrs):
        self.adapter_class = GoogleOAuth2Adapter
        return super().validate(attrs)

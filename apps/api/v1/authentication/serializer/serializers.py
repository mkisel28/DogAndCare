from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.password_validation import validate_password
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import LoginSerializer
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from apps.authentication.models import EmailVerificationCode
import re
import random
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from allauth.account.adapter import get_adapter


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


class PasswordResetConfirmSerializer(serializers.Serializer):
    new_password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    new_password2 = serializers.CharField(write_only=True, required=True)

    def validate(self, data):
        if data["new_password"] != data["new_password2"]:
            raise serializers.ValidationError("Passwords do not match")
        return data


class CustomLoginSerializer(LoginSerializer):
    username = None
    email = serializers.EmailField(required=True)

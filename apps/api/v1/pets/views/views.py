from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema


from apps.authentication.models import EmailVerificationCode
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from apps.authentication.tasks import send_verification_email

from apps.api.v1.pets.serializer.serializers import (
    BreedSerializer,
    CreatePetSerializer,
    PetSerializer,
    PetsSerializer,
    TemperamentSerializer,
)
from apps.pets.models import Breed, Pet, Temperament


from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
    OpenApiParameter,
)
from drf_spectacular.types import OpenApiTypes


@extend_schema(tags=["User Pets Management"])
class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user).order_by("-created_at")

    def get_serializer(self, *args, **kwargs):
        if self.action in ["list", "retrieve"]:
            return PetsSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    @extend_schema(summary="Добавление питомца")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(summary="Получение питомцев пользователя")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="Получение питомца по id пользователя")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


@extend_schema(tags=["Reference Data"])
class BreedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer

    @extend_schema(summary="Получение списка пород")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="Получение породы по id")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)


@extend_schema(tags=["Reference Data"])
class TemperamentViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Temperament.objects.all()
    serializer_class = TemperamentSerializer

    @extend_schema(summary="Получение списка темпераментов")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="Получение темперамента по id")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

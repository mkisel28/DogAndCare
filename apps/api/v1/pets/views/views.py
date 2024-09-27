from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema

from apps.api.v1.pets.serializer.serializers import (
    BreedSerializer,
    PetCreateSerializer,
    PetsSerializer,
    TemperamentSerializer,
)
from apps.pets.models import Breed, Pet, Temperament

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
)


@extend_schema(tags=["User Pets Management"])
class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetCreateSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Pet.objects.filter(owner=self.request.user).order_by("-created_at")

    def get_serializer(self, *args, **kwargs):
        if self.action in ["list", "retrieve"]:
            return PetsSerializer(*args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    @extend_schema(
        summary="Добавление питомца",
        description=(
            "Добавление нового питомца пользователю.\n\n"
            "Все поля могут быть `null` или отсутствовать.\n\n"
            "Аутентифицированный пользователь автоматически назначается владельцем питомца."
        ),
        responses={
            201: PetCreateSerializer,
            400: OpenApiResponse(
                description="Некорректные данные или ошибки валидации"
            ),
            401: OpenApiResponse(description="Пользователь не аутентифицирован"),
        },
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(summary="Получение питомцев пользователя")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="Получение питомца по его id")
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

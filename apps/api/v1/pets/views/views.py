from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema
from rest_framework.decorators import permission_classes
from apps.api.v1.health.serializer.serializers import DailyLogSerializer
from apps.api.v1.health.views.views import IsOwner
from apps.api.v1.pets.serializer.serializers import (
    BreedSerializer,
    # PetCreateSerializer,
    PetSerializer,
    TemperamentSerializer,
)
from apps.health.models import DailyLog
from apps.pets.models import Breed, Pet, Temperament

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
)
from rest_framework.decorators import action


@extend_schema(tags=["User Pets Management"])
class PetViewSet(viewsets.ModelViewSet):
    queryset = Pet.objects.all()
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Pet.objects.filter().select_related("breed").order_by("-created_at")

    # def get_serializer(self, *args, **kwargs):
    #     if self.action in ["list", "retrieve"]:
    #         return PetsSerializer(*args, **kwargs)
    #     return super().get_serializer(*args, **kwargs)

    @extend_schema(
        summary="Добавление питомца",
        description=(
            "Добавление нового питомца пользователю.\n\n"
            "Все поля могут быть `null` или отсутствовать.\n\n"
            "Аутентифицированный пользователь автоматически назначается владельцем питомца."
        ),
        responses={
            201: PetSerializer,
            400: OpenApiResponse(
                description="Некорректный запрос",
                response=PetSerializer,
                examples=[
                    OpenApiExample(
                        name="Дата рождения в будущем",
                        value={
                            "birth_date": ["The birth date cannot be in the future."],
                        },
                    ),
                    OpenApiExample(
                        name="Питомец не может быть старше 50 лет",
                        value={
                            "birth_date": ["The pet can not be older than 50 years."],
                        },
                    ),
                    OpenApiExample(
                        name="Некорректный формат файла",
                        value={
                            "avatar": [
                                "The submitted data was not a file. Check the encoding type on the form."
                            ],
                        },
                    ),
                ],
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

    @extend_schema(
        summary="Управление симптомами питомца",
        request=DailyLogSerializer,
        responses=DailyLogSerializer,
    )
    @action(
        detail=True,
        methods=["post", "delete", "get", "patch"],
        url_path="symptoms",
        url_name="manage_symptoms",
    )
    def manage_symptoms(self, request, pk=None):
        self.check_permissions(request)
        self.check_object_permissions(request, self.get_object())
        pet = Pet.objects.get(pk=pk)

        if request.method == "GET":
            log = DailyLog.get_today_log(pet=pet)
            serializer = DailyLogSerializer(log)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == "POST":
            create = DailyLogSerializer(data=request.data, context={"pet_id": pk})
            create.is_valid(raise_exception=True)
            create.save()
            return Response(create.data, status=status.HTTP_201_CREATED)

        elif request.method == "DELETE":
            log = DailyLog.get_today_log(pet=pet)
            log.symptoms.clear()
            serializer = DailyLogSerializer(log)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == "PATCH":
            log = DailyLog.get_today_log(pet=pet)
            log.symptoms.set(request.data["symptoms_id"])
            serializer = DailyLogSerializer(log)
            return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(tags=["Reference Data"])
class BreedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    authentication_classes = []

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
    authentication_classes = []

    @extend_schema(summary="Получение списка темпераментов")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="Получение темперамента по id")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

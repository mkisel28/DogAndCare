from rest_framework import mixins, viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from drf_spectacular.utils import (
    extend_schema,
    OpenApiResponse,
    OpenApiExample,
    OpenApiParameter,
)

from apps.api.v1.health.serializer.serializers import DailyLogSerializer
from apps.api.v1.pets.serializer.serializers import (
    BreedSerializer,
    PetSerializer,
    TemperamentSerializer,
)
from apps.health.models import DailyLog
from apps.pets.models import Breed, Pet, Temperament
from apps.api.v1.health.views.views import IsOwner


@extend_schema(tags=["User Pets Management"])
class PetViewSet(viewsets.ModelViewSet):
    serializer_class = PetSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    queryset = Pet.objects.none()

    def get_queryset(self):
        return (
            Pet.objects.filter(owner=self.request.user)
            .select_related("breed")
            .order_by("-created_at")
        )

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

    # @extend_schema(
    #     summary="Управление симптомами питомца",
    #     request=DailyLogSerializer,
    #     responses=DailyLogSerializer,
    #     parameters=[
    #         OpenApiParameter(
    #             name="timezone",
    #             description="Часовой пояс пользователя (например, Europe/Minsk)",
    #             required=False,
    #             type=str,
    #             location=OpenApiParameter.QUERY,
    #         ),
    #     ],
    # )
    # @action(
    #     detail=True,
    #     methods=["post", "delete", "get", "patch"],
    #     url_path="symptoms",
    #     url_name="manage_symptoms",
    # )
    # def manage_symptoms(self, request, pk=None):
    #     # Получаем объект питомца, к которому относятся симптомы
    #     pet = self.get_object()

    #     user_timezone = request.GET.get("timezone", None)

    #     # Здесь используем другой queryset для управления логами симптомов
    #     log_queryset = DailyLog.objects.filter(pet=pet).select_related("pet").prefetch_related("symptoms", "symptoms__category")

    #     if request.method == "GET":
    #         log = self._get_log(pet, user_timezone)
    #         serializer = DailyLogSerializer(log_queryset.get(pk=log.pk))
    #         return Response(serializer.data, status=status.HTTP_200_OK)

    #     elif request.method == "POST":
    #         create = DailyLogSerializer(
    #             data=request.data, context={"pet_id": pk, "timezone": user_timezone}
    #         )
    #         create.is_valid(raise_exception=True)
    #         create.save()
    #         return Response(create.data, status=status.HTTP_201_CREATED)

    #     elif request.method == "DELETE":
    #         log = self._get_log(pet, user_timezone)
    #         log.symptoms.clear()
    #         serializer = DailyLogSerializer(log_queryset.get(pk=log.pk))
    #         return Response(serializer.data, status=status.HTTP_200_OK)

    #     elif request.method == "PATCH":
    #         log = self._get_log(pet, user_timezone)
    #         log.symptoms.set(request.data["symptoms_id"])
    #         serializer = DailyLogSerializer(log_queryset.get(pk=log.pk))
    #         return Response(serializer.data, status=status.HTTP_200_OK)

    # def _get_log(self, pet, user_timezone=None):
    #     # Здесь используем питомца, полученного в методе manage_symptoms
    #     log = DailyLog.get_today_log(pet=pet, user_timezone=user_timezone)
    #     return log


@extend_schema(
    summary="Управление симптомами питомца",
    tags=["Health"],
    request=DailyLogSerializer,
    responses=DailyLogSerializer,
    parameters=[
        OpenApiParameter(
            name="timezone",
            description="Часовой пояс пользователя (например, Europe/Minsk)",
            required=False,
            type=str,
            location=OpenApiParameter.QUERY,
        ),
    ],
)
class SymptomLogViewSet(
    mixins.ListModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = DailyLogSerializer
    permission_classes = [IsAuthenticated, IsOwner]
    pagination_class = None
    queryset = DailyLog.objects.all()

    def _get_log(self, pk, user_timezone=None):
        return DailyLog.get_today_log(pk, user_timezone=user_timezone)

    def list(self, request, *args, **kwargs):
        user_timezone = request.GET.get("timezone", None)
        log = self._get_log(kwargs.get("pet_pk"), user_timezone=user_timezone)
        serializer = self.get_serializer(log)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request, *args, **kwargs):
        user_timezone = request.GET.get("timezone", None)
        serializer = self.get_serializer(
            data=request.data,
            context={"timezone": user_timezone, "pet_id": kwargs.get("pet_pk")},
        )
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(
        detail=False, methods=["delete"], url_path="clear", url_name="clear_symptoms"
    )
    def clear_all_symptom(self, request, *args, **kwargs):
        """
        Очищает все симптомы для указанного питомца.
        """
        user_timezone = request.GET.get("timezone", None)
        log = self._get_log(kwargs.get("pet_pk"), user_timezone=user_timezone)

        if not log:
            return Response(
                {"detail": "DailyLog not found."}, status=status.HTTP_404_NOT_FOUND
            )

        log.symptoms.clear()
        log.save()
        return Response(
            {"detail": "All symptoms removed successfully."}, status=status.HTTP_200_OK
        )

    # TODO: Добавить документацию к методам add_symptom и remove_symptom\
    # TODO: Использовать Timezone
    @action(detail=False, methods=["patch"], url_path="add", url_name="add_symptom")
    def add_symptom(self, request, *args, **kwargs):
        """
        Добавляет указанные симптом для указанного питомца.


        """
        symptom_id = request.data.get("symptoms_id", None)
        log = self._get_log(kwargs.get("pet_pk"), user_timezone=None)

        if not log:
            return Response(
                {"detail": "DailyLog not found."}, status=status.HTTP_404_NOT_FOUND
            )
            # log = DailyLog.get_today_log(kwargs.get("pet_pk"), user_timezone=None)

        log.add_symptoms(symptom_id)
        log.save()

        return Response(
            {"detail": "Symptom added successfully."}, status=status.HTTP_200_OK
        )

    @action(
        detail=False, methods=["patch"], url_path="remove", url_name="remove_symptom"
    )
    def remove_symptom(self, request, *args, **kwargs):
        """
        Удаляет указанные симптом для указанного питомца.
        """
        symptom_id = request.data.get("symptoms_id", None)

        log = self._get_log(kwargs.get("pet_pk"), user_timezone=None)
        if not log:
            return Response(
                {"detail": "DailyLog not found."}, status=status.HTTP_404_NOT_FOUND
            )
            # log = DailyLog.get_today_log(kwargs.get("pet_pk"), user_timezone=None)

        log.remove_symptoms(symptom_id)
        log.save()

        return Response(
            {"detail": "Symptom removed successfully."}, status=status.HTTP_200_OK
        )


@extend_schema(tags=["Reference Data"])
class BreedViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Breed.objects.all()
    serializer_class = BreedSerializer
    authentication_classes = []
    pagination_class = None

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
    pagination_class = None

    @extend_schema(summary="Получение списка темпераментов")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(summary="Получение темперамента по id")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

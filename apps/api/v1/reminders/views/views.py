from django_filters import rest_framework as filters
from drf_spectacular.utils import OpenApiExample, OpenApiResponse, extend_schema
from rest_framework import filters as drf_filters
from rest_framework import permissions, viewsets

from apps.api.v1.reminders.filters import ReminderFilter
from apps.api.v1.reminders.serializer.serializers import (
    ReminderCategorySerializer,
    ReminderSerializer,
)
from apps.reminders.models import Reminder, ReminderCategory
from utils.pagintaion import CustomPageNumberPagination


@extend_schema(tags=["Reminders"])
class ReminderViewSet(viewsets.ModelViewSet):
    queryset = (
        Reminder.objects.all()
        .select_related("owner", "reminder_type", "reminder_type__category")
        .prefetch_related("pets")
    )
    serializer_class = ReminderSerializer
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPageNumberPagination
    filter_backends = [
        filters.DjangoFilterBackend,
    ]
    filterset_class = ReminderFilter


    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user)

    @extend_schema(
        summary="Получение списка напоминаний",
        description="Получение списка всех напоминаний пользователя.",
        responses={
            200: ReminderSerializer(many=True),
            401: OpenApiResponse(description="Пользователь не аутентифицирован"),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Создание напоминания",
        description=(
            "Создание нового напоминания для питомца/питомцев.\n\n"
            "Все поля могут быть заполнены с учетом логики создания напоминаний,\n\n"
            "питомцы передаются в виде их ID, а также можно указать частоту повторений "
            "напоминания в минутах для повторяющихся напоминаний.\n\n"
            "Аутентифицированный пользователь автоматически назначается владельцем напоминания."
        ),
        request=ReminderSerializer,
        responses={
            201: ReminderSerializer,
            400: OpenApiResponse(
                description="Некорректный запрос",
                response=ReminderSerializer,
                examples=[
                    OpenApiExample(
                        name="Дата напоминания в прошлом",
                        value={
                            "reminder_time": [
                                "The reminder time cannot be in the past.",
                            ],
                        },
                    ),
                    OpenApiExample(
                        name="Питомец не принадлежит пользователю",
                        value={
                            "pets": ["Pet does not belong to you."],
                        },
                    ),
                    OpenApiExample(
                        name="Не указана частота для повторяющихся напоминаний",
                        value={
                            "frequency_in_minutes": [
                                "This field is required for recurring reminders.",
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

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @extend_schema(
        summary="Получение напоминания",
        description="Получение информации о конкретном напоминании.",
        responses={
            200: ReminderSerializer,
            401: OpenApiResponse(description="Пользователь не аутентифицирован"),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(
        summary="Обновление напоминания",
        description="Обновление информации о конкретном напоминании.",
        request=ReminderSerializer,
        responses={
            200: ReminderSerializer,
            400: OpenApiResponse(
                description="Некорректный запрос",
                response=ReminderSerializer,
                examples=[
                    OpenApiExample(
                        name="Дата напоминания в прошлом",
                        value={
                            "reminder_time": [
                                "The reminder time cannot be in the past.",
                            ],
                        },
                    ),
                    OpenApiExample(
                        name="Питомец не принадлежит пользователю",
                        value={
                            "pets": ["Pet does not belong to you."],
                        },
                    ),
                    OpenApiExample(
                        name="Не указана частота для повторяющихся напоминаний",
                        value={
                            "frequency_in_minutes": [
                                "This field is required for recurring reminders.",
                            ],
                        },
                    ),
                ],
            ),
            401: OpenApiResponse(description="Пользователь не аутентифицирован"),
        },
    )
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(
        summary="Частичное обновление напоминания",
        description="Частичное обновление информации о конкретном напоминании.",
        request=ReminderSerializer,
        responses={
            200: ReminderSerializer,
            400: OpenApiResponse(
                description="Некорректный запрос",
                response=ReminderSerializer,
                examples=[
                    OpenApiExample(
                        name="Дата напоминания в прошлом",
                        value={
                            "reminder_time": [
                                "The reminder time cannot be in the past.",
                            ],
                        },
                    ),
                    OpenApiExample(
                        name="Питомец не принадлежит пользователю",
                        value={
                            "pets": ["Pet does not belong to you."],
                        },
                    ),
                    OpenApiExample(
                        name="Не указана частота для повторяющихся напоминаний",
                        value={
                            "frequency_in_minutes": [
                                "This field is required for recurring reminders.",
                            ],
                        },
                    ),
                ],
            ),
            401: OpenApiResponse(description="Пользователь не аутентифицирован"),
        },
    )
    def partial_update(self, request, *args, **kwargs):
        return super().partial_update(request, *args, **kwargs)


@extend_schema(tags=["Reference Data"])
class ReminderCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ReminderCategory.objects.all().prefetch_related("types")
    serializer_class = ReminderCategorySerializer
    authentication_classes = []
    pagination_class = None
    permission_classes = [permissions.AllowAny]

    @extend_schema(
        summary="Получение списка категорий напоминаний с типами",
        description="Получение списка всех категорий напоминаний.",
        responses={
            200: ReminderCategorySerializer(many=True),
            401: OpenApiResponse(description="Пользователь не аутентифицирован"),
        },
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(
        summary="Получение категории напоминания",
        description="Получение информации о конкретной категории напоминания.",
        responses={
            200: ReminderCategorySerializer,
            401: OpenApiResponse(description="Пользователь не аутентифицирован"),
        },
    )
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

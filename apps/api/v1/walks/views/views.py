import datetime

from django.utils import timezone
from drf_spectacular.utils import (
    OpenApiExample,
    OpenApiParameter,
    OpenApiResponse,
    extend_schema,
)
from rest_framework import mixins, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.api.v1.walks.serializer.serializers import WalkSerializer, WalkStatsSerializer
from apps.walks.models import Walk, WalkStats
from utils.pagintaion import CustomPageNumberPagination


@extend_schema(
    tags=["Walks"],
    summary="Управление прогулками для питомцев",
)
class WalkViewSet(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    """WalkViewSet управляет созданием, получением, обновлением, удалением и перечислением экземпляров Walk для конкретного питомца.

    - `create` endpoint позволяет аутентифицированным пользователям создавать новую прогулку для конкретного питомца.
    - `retrieve` endpoint позволяет пользователям получать детали конкретной прогулки по ID прогулки.
    - `update` endpoint позволяет модифицировать детали прогулки по ID прогулки.
    - `delete` endpoint удаляет конкретную прогулку по ID прогулки.
    - `list` endpoint возвращает все прогулки, связанные с данным питомцем и пользователем.
    """

    queryset = Walk.objects.select_related("pet", "owner").all()
    serializer_class = WalkSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        pet_pk = self.kwargs.get("pet_pk")
        return self.queryset.filter(owner=self.request.user, pet__id=pet_pk)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user, pet_id=self.kwargs.get("pet_pk"))


@extend_schema(
    tags=["Walks"],
    summary="Статистика прогулок для питомцев",
)
class WalkStatsViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = WalkStats.objects.select_related("pet", "pet__owner").all()
    serializer_class = WalkStatsSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPageNumberPagination

    def get_queryset(self):
        pet_pk = self.kwargs.get("pet_pk")
        return self.queryset.filter(pet__owner=self.request.user, pet__id=pet_pk)

    @extend_schema(
        summary="Ежедневная статистика прогулок",
        responses={
            200: WalkStatsSerializer,
            400: OpenApiResponse(
                description="Некорректный запрос",
                response=WalkStatsSerializer,
                examples=[
                    OpenApiExample(
                        name="Дата невалидна",
                        value={"date": "Date has wrong format. Use YYYY-MM-DD."},
                    ),
                ],
            ),
            401: OpenApiResponse(description="Необходима аутентификация пользователя"),
            404: OpenApiResponse(
                description="Статистика прогулок не найдена",
                response=WalkStatsSerializer,
                examples=[
                    OpenApiExample(
                        name="Статистика прогулок не найдена",
                        value={
                            "detail": "Stat for the given date not found.",
                        },
                    ),
                ],
            ),
        },
        parameters=[
            OpenApiParameter(
                name="date",
                required=False,
                type=datetime.date,
                description="Дата, для которой необходимо получить статистику прогулок. По умолчанию используется текущая дата.",
            ),
        ],
    )
    @action(detail=False, methods=["get"], url_path="daily")
    def daily_stats(self, request, *args, **kwargs):
        """Получить ежедневную статистику для конкретного питомца по ID.

        Параметры:
        - `pet_pk` (обязательный): Первичный ключ питомца.
        - `date` (необязательный): Дата, для которой требуется статистика, по умолчанию текущая дата.

        Возвращает ежедневную статистику прогулок для конкретного питомца.
        """
        pet_id = kwargs.get("pet_pk")
        date_str = request.query_params.get("date", timezone.now().date())
        try:
            date = datetime.datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"date": "Date has wrong format. Use YYYY-MM-DD."},
                status=400,
            )

        if not pet_id:
            return Response({"pet_id": "This field is required"}, status=400)
        try:
            stat = WalkStats.objects.get(pet__id=pet_id, date=date)
        except WalkStats.DoesNotExist:
            return Response(
                {"detail": "Stat for the given date not found."},
                status=404,
            )

        serializer = WalkStatsSerializer(stat)
        return Response(serializer.data)

    @extend_schema(
        summary="Недельная статистика прогулок по дням",
        responses={
            200: WalkStatsSerializer,
            400: OpenApiResponse(
                description="Некорректный запрос",
                response=WalkStatsSerializer,
                examples=[
                    OpenApiExample(
                        name="Неверный диапазон дат",
                        value={
                            "date": "End date cannot be before start date",
                        },
                    ),
                    OpenApiExample(
                        name="Питомец не найден",
                        value={
                            "pet_pk": "This field is required",
                        },
                    ),
                ],
            ),
        },
        parameters=[
            OpenApiParameter(
                name="start_date",
                required=False,
                type=datetime.date,
                description="Дата начала диапазона, по умолчанию используется текущая дата.",
            ),
            OpenApiParameter(
                name="end_date",
                required=False,
                type=datetime.date,
                description="Дата окончания диапазона. По умолчанию 6 дней до даты начала.",
            ),
        ],
    )
    @action(detail=False, methods=["get"], url_path="weekly")
    def weekly_stats(self, request, *args, **kwargs):
        """Получить недельную статистику для конкретного питомца по ID в заданном диапазоне дат.

        Параметры:
        - `pet_pk` (обязательный): Первичный ключ питомца.
        - `start_date` (необязательный): Дата начала диапазона.
        - `end_date` (необязательный): Дата окончания диапазона (по умолчанию 7 дней до `start_date`).

        Возвращает недельную статистику прогулок для питомца.
        """
        pet_id = kwargs.get("pet_pk")
        end_date_str = request.query_params.get("end_date", timezone.now().date())
        start_date_str = request.query_params.get(
            "start_date",
            (timezone.now() - datetime.timedelta(days=6)).date(),
        )

        try:
            end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d").date()
            start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d").date()
        except ValueError:
            return Response(
                {"date": "Date has wrong format. Use YYYY-MM-DD."},
                status=400,
            )

        if end_date < start_date:
            return Response(
                {"date": "End date cannot be before start date"},
                status=400,
            )
        if not pet_id:
            return Response({"pet_pk": "This field is required"}, status=400)

        stats = WalkStats.objects.filter(
            pet__id=pet_id,
            date__range=(start_date, end_date),
        )
        serializer = WalkStatsSerializer(stats, many=True)
        return Response(serializer.data)

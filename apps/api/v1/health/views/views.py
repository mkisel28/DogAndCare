from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.api.v1.health.serializer.serializers import (
    DailyLogSerializer,
    SymptomCategorySerializer,
    SymptomWithCategorySerializer,
)
from apps.health.models import DailyLog, Symptom, SymptomCategory
from apps.pets.models import Pet


class IsOwner(permissions.BasePermission):
    """Разрешение, позволяющее пользователю взаимодействовать только со своими объектами."""

    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user


@extend_schema(
    tags=["Reference Data"],
    summary="Получение списка доступных категорий симптомов",
)
class SymptomCategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SymptomCategory.objects.prefetch_related("symptoms").all()
    serializer_class = SymptomCategorySerializer
    pagination_class = None
    authentication_classes = []


@extend_schema(tags=["Reference Data"], summary="Получение списка доступных симптомов")
class SymptomViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = (
        Symptom.objects.select_related("category")
        .prefetch_related("category__symptoms")
        .all()
    )
    serializer_class = SymptomWithCategorySerializer
    pagination_class = None
    authentication_classes = []


class DailyLogViewSet(viewsets.ModelViewSet):
    serializer_class = DailyLogSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return (
            DailyLog.objects.filter(pet__owner=self.request.user)
            .select_related("pet")
            .prefetch_related("symptoms")
        )

    @action(detail=False, methods=["get"], url_path="today")
    def today(self, request):
        pet_id = request.query_params.get("pet_id")
        if pet_id:
            pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
        else:
            pet = request.user.pets.first()
            if not pet:
                return Response(
                    {"detail": "У пользователя нет питомцев."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        log = DailyLog.get_today_log(pet)
        serializer = self.get_serializer(log)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="add-symptoms")
    def add_symptoms(self, request, pk=None):
        log = self.get_object()
        symptom_ids = request.data.get("symptoms", [])
        if not isinstance(symptom_ids, list):
            return Response(
                {"detail": "Симптомы должны быть списком ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        log.add_symptoms(symptom_ids)
        serializer = self.get_serializer(log)
        return Response(serializer.data)

    @action(detail=True, methods=["post"], url_path="remove-symptoms")
    def remove_symptoms(self, request, pk=None):
        log = self.get_object()
        symptom_ids = request.data.get("symptoms", [])
        if not isinstance(symptom_ids, list):
            return Response(
                {"detail": "Симптомы должны быть списком ID."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        log.remove_symptoms(symptom_ids)
        serializer = self.get_serializer(log)
        return Response(serializer.data)

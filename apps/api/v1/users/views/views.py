from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from apps.api.v1.users.serializer.serializers import (
    UserSerializer,
)


@extend_schema(tags=["User Management"])
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = None

    @extend_schema(summary="Получение текущего пользователя")
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

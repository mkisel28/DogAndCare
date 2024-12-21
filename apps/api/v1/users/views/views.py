from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.api.v1.users.serializer.serializers import (
    UserSerializer,
)


@extend_schema(tags=["User Management"])
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UserSerializer

    @extend_schema(summary="Получение текущего пользователя")
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    @extend_schema(summary="Частичное обновление текущего пользователя")
    def patch(self, request, *args, **kwargs):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=200)

    @extend_schema(summary="Удаление текущего пользователя")
    def delete(self, request, *args, **kwargs):
        request.user.delete()
        return Response({"detail": "User deleted"}, status=204)

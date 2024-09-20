from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema

from apps.api.v1.authentication.serializer.serializers import CodeSerializer
from apps.api.v1.users.serializer.serializers import (
    UserSerializer,
)
from apps.authentication.models import EmailVerificationCode
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from apps.authentication.tasks import send_verification_email


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
        return Response(serializer.data)


@extend_schema(tags=["User Management"])
class RequestDeleteUserView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        summary="Запрос на удаление текущего пользователя (отправка кода на почту)"
    )
    def post(self, request, *args, **kwargs):
        self._send_verification_code(request.user, request)
        return Response({"detail": "Code sent to your email"}, status=200)

    def _send_verification_code(self, user, request):
        _, code = EmailVerificationCode.create_code(user)
        context = {
            "user": user,
            "code": code,
            "request": request,
        }
        html_message = render_to_string(
            "account/email/account_deletion_confirmation_email.html", context
        )
        plain_message = strip_tags(html_message)

        send_verification_email.delay(
            subject=f"[{code}] Ваш код подтверждения для удаления аккаунта",
            plain_message=plain_message,
            from_email=None,
            recipient_list=[user.email],
            html_message=html_message,
        )


@extend_schema(tags=["User Management"])
class ConfirmDeleteUserView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CodeSerializer

    @extend_schema(summary="Подтверждение удаления текущего пользователя")
    def post(self, request, *args, **kwargs):
        code = request.data.get("code")

        verification_code = EmailVerificationCode.objects.filter(
            user=request.user, code=code, is_used=False
        ).first()

        if not verification_code:
            return Response({"detail": "Invalid confirmation code."}, status=400)

        if verification_code.is_expired():
            return Response(
                {"detail": "The confirmation code has expired."}, status=400
            )

        verification_code.mark_as_used()
        request.user.delete()
        return Response({"detail": "User deleted"}, status=204)

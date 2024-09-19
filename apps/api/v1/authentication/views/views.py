from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from rest_framework.exceptions import ValidationError
from django.core.mail import send_mail as send_email

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import (
    RefreshToken,
    OutstandingToken,
    BlacklistedToken,
)
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from apps.api.v1.authentication.serializer.serializers import (
    CustomRegisterSerializer,
    PasswordResetSerializer,
    PasswordResetConfirmSerializer,
    VerifyEmailCodeSerializer,
)
from apps.api.v1.users.serializer.serializers import (
    AuthUserSerializer,
    LogoutSerializer,
    UserSerializer,
)

from dj_rest_auth.registration.views import VerifyEmailView, RegisterView

from apps.authentication.models import EmailVerificationCode
from allauth.account.models import EmailAddress
from drf_spectacular.utils import (
    extend_schema,
    OpenApiExample,
    OpenApiResponse,
    OpenApiParameter,
)
from rest_framework.decorators import action

from apps.authentication.tasks import send_verification_email


@extend_schema(
    tags=["Authentication"],
    summary="Регистрация пользователя",
    request=CustomRegisterSerializer,
    responses={
        status.HTTP_201_CREATED: OpenApiResponse(
            description="Пользователь успешно зарегистрирован. На указанный email отправлен код подтверждения.",
            response={"user_id": 1, "detail": "Verification e-mail sent."},
            examples=[
                OpenApiExample(
                    name="Пример успешного ответа",
                    summary="Пользователь успешно зарегистрирован",
                    value={
                        "user_id": 1,
                        "detail": "Verification e-mail sent.",
                    },
                ),
            ],
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description="Ошибки валидации при регистрации.",
            response=dict,
            examples=[
                OpenApiExample(
                    name="Неверный формат email",
                    summary="Неверный формат email",
                    value={
                        "email": ["Enter a valid email address."],
                    },
                ),
                OpenApiExample(
                    name="Пароль слишком короткий",
                    summary="Пароль слишком короткий",
                    value={
                        "password1": [
                            "This password is too short. It must contain at least 8 characters."
                        ],
                    },
                ),
                OpenApiExample(
                    name="Пароли не совпадают",
                    summary="Пароли не совпадают",
                    value={
                        "non_field_errors": ["The two password fields didn't match."],
                    },
                ),
                OpenApiExample(
                    name="Пользователь с таким email уже существует",
                    summary="Пользователь с таким email уже существует",
                    value={
                        "email": [
                            "A user is already registered with this e-mail address."
                        ]
                    },
                ),
            ],
        ),
    },
)
class CustomRegisterView(RegisterView):
    """
    Регистрация нового пользователя.
    Требуется предоставить `email`, `password1` и `password2`.
    Поля `first_name` и `last_name` являются необязательными.

    - email: обязательное поле. Только английские буквы и цифры.
    - password1: обязательное поле для пароля, минимум 8 символов

    **После успешной регистрации пользователю отправляется письмо с подтверждением.**

    **Важно:** В ответе возвращается `user_id`, который необходимо использовать для подтверждения электронной почты.
    """

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        data = self.get_response_data(user)

        if data:
            user_id = user.id
            data["user_id"] = user_id
            response = Response(
                data,
                status=status.HTTP_201_CREATED,
                headers=headers,
            )
        else:
            response = Response(status=status.HTTP_204_NO_CONTENT, headers=headers)

        return response


from rest_framework.generics import CreateAPIView
from allauth.account.models import EmailAddress
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from rest_framework import mixins, viewsets


@extend_schema(
    tags=["Authentication"],
    request=CustomRegisterSerializer,
    summary="Запрос на отправку кода для регистрации или авторизации через email",
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=dict,
            description="Пользователь существует, код для авторизации отправлен на email.",
            examples=[
                OpenApiExample(
                    name="Код отправлен для авторизации",
                    summary="Пользователь существует и код отправлен для входа",
                    value={"detail": "Verification code sent to email"},
                )
            ],
        ),
        status.HTTP_201_CREATED: OpenApiResponse(
            response=dict,
            description="Пользователь зарегистрирован, код для подтверждения отправлен на email.",
            examples=[
                OpenApiExample(
                    name="Пользователь зарегистрирован",
                    summary="Создан новый пользователь и отправлен код для подтверждения",
                    value={"detail": "User registered and verification code sent"},
                )
            ],
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=dict,
            description="Ошибки валидации email.",
            examples=[
                OpenApiExample(
                    name="Некорректный email",
                    summary="Неверный формат email или другие ошибки валидации",
                    value={"email": ["Enter a valid email address."]},
                ),
                OpenApiExample(
                    name="Email не указан",
                    summary="Email не указан в запросе",
                    value={"email": ["This field is required."]},
                ),
            ],
        ),
    },
)
class EmailAuthRequestView(mixins.CreateModelMixin, viewsets.GenericViewSet):
    """
    Запрос на регистрацию или авторизацию пользователя через email.

    В зависимости от состояния пользователя, API выполняет две задачи:

    1. **Авторизация**: Если пользователь с указанным email уже существует и его почта подтверждена, отправляется код для входа. Ответ имеет статус 200 (OK).
    2. **Регистрация**: Если пользователь не существует или его почта ещё не подтверждена, создается новый пользователь и отправляется код для подтверждения почты. Ответ имеет статус 201 (Created).

    Процесс работы:
    - Пользователь отправляет email в запросе.
    - Система отправляет 6-значный код на указанный email для подтверждения, который будет использован для последующей авторизации.

    Примеры ответов:
    - **HTTP 200**: Если email уже подтвержден, код для авторизации отправляется на указанный email.
    - **HTTP 201**: Если пользователь только что зарегистрирован или его email ещё не был подтвержден, код для подтверждения отправляется на email.

    Ошибки:
    - **HTTP 400**: В случае ошибки валидации email.
    """

    serializer_class = CustomRegisterSerializer
    permission_classes = [AllowAny]

    @extend_schema(tags=["Authentication"], methods=["post"])
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            email = request.data["email"]
        except KeyError:
            return Response(
                {"email": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            email_address = EmailAddress.objects.get(email=email)
            user = email_address.user
            if email_address.verified:
                status_code = status.HTTP_200_OK
                data = {"detail": "Verification code sent to email"}
            else:
                status_code = status.HTTP_201_CREATED
                data = {"detail": "User registered and verification code sent"}
        except EmailAddress.DoesNotExist:
            serializer.is_valid(raise_exception=True)
            email = serializer.validated_data["email"]
            serializer.save(request)
            user = EmailAddress.objects.get(email=email).user
            status_code = status.HTTP_201_CREATED
            data = {"detail": "User registered and verification code sent"}

        self._send_verification_code(user, request)
        return Response(data, status=status_code)

    @extend_schema(
        tags=["Authentication"],
        methods=["post"],
        summary="Повторная отправка кода подтверждения на email",
        description="Отправляет новый код подтверждения на указанный email.",
        responses={
            status.HTTP_200_OK: OpenApiResponse(
                response=dict,
                description="Код подтверждения отправлен на email",
                examples=[
                    OpenApiExample(
                        name="Код отправлен",
                        summary="Код подтверждения отправлен на email",
                        value={"detail": "Verification code sent to email"},
                    )
                ],
            ),
            status.HTTP_400_BAD_REQUEST: OpenApiResponse(
                response=dict,
                description="Email не указан",
                examples=[
                    OpenApiExample(
                        name="Email не указан",
                        summary="Email не указан в запросе",
                        value={"email": ["This field is required."]},
                    ),
                    OpenApiExample(
                        name="Email не найден",
                        summary="Email не найден",
                        value={"email": ["Email not found."]},
                    ),
                ],
            ),
            status.HTTP_404_NOT_FOUND: OpenApiResponse(
                response=dict,
                description="Email не найден",
                examples=[
                    OpenApiExample(
                        name="Email не найден",
                        summary="Email не найден",
                        value={"email": ["Email not found."]},
                    ),
                ],
            ),
        },
    )
    @action(detail=False, methods=["post"])
    def resend_code(self, request, *args, **kwargs):
        email = request.data.get("email", None)
        if not email:
            return Response(
                {"email": ["This field is required."]},
                status=status.HTTP_400_BAD_REQUEST,
            )
        try:
            email_address = EmailAddress.objects.get(email=email)
            user = email_address.user
        except EmailAddress.DoesNotExist:
            return Response(
                {"email": ["Email not found."]},
                status=status.HTTP_404_NOT_FOUND,
            )

        self._send_verification_code(user, request)
        return Response(
            {"detail": "Verification code sent to email"}, status=status.HTTP_200_OK
        )

    def _send_verification_code(self, user, request):
        """Helper method to generate code and send email."""
        _, code = EmailVerificationCode.create_code(user)
        context = {
            "user": user,
            "code": code,
            "request": request,
        }
        html_message = render_to_string(
            "account/email/confirmation_email.html", context
        )
        plain_message = strip_tags(html_message)

        send_verification_email.delay(
            subject=f"[{code}] Your Verification Code for Dog&Care",
            plain_message=plain_message,
            from_email=None,
            recipient_list=[user.email],
            html_message=html_message,
        )


@extend_schema(
    tags=["Authentication"],
    request=VerifyEmailCodeSerializer,
    summary="Подтверждение email и авторизация через JWT",
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=AuthUserSerializer,
            description="Пользователь успешно авторизован. Возвращаются данные пользователя и JWT токены.",
            examples=[
                OpenApiExample(
                    name="Успешная авторизация",
                    summary="Email подтвержден или пользователь авторизован",
                ),
            ],
        ),
        status.HTTP_201_CREATED: OpenApiResponse(
            response=AuthUserSerializer,
            description="Email успешно подтвержден, и пользователь авторизован. Возвращаются данные пользователя и JWT токены.",
            examples=[
                OpenApiExample(
                    name="Успешное подтверждение",
                    summary="Email подтвержден и JWT токены возвращены",
                ),
            ],
        ),
        status.HTTP_404_NOT_FOUND: OpenApiResponse(
            description="Пользователь не найден.",
            response=dict,
            examples=[
                OpenApiExample(
                    name="Пользователь не найден",
                    summary="User not found",
                    value={"detail": "User not found."},
                )
            ],
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            description="Ошибки при подтверждении email.",
            response=dict,
            examples=[
                OpenApiExample(
                    name="Неверный код подтверждения",
                    summary="Invalid confirmation code",
                    value={"detail": "Invalid confirmation code."},
                ),
                OpenApiExample(
                    name="Код подтверждения истек",
                    summary="The confirmation code has expired",
                    value={"detail": "The confirmation code has expired."},
                ),
            ],
        ),
    },
)
class CustomVerifyEmailView(VerifyEmailView):
    """
    Подтверждение email и авторизация через JWT.

    Этот API выполняет две основные функции:

    1. **Подтверждение email**:
       Если пользователь только что зарегистрирован и его почта ещё не подтверждена, он отправляет 6-значный код для подтверждения. После успешного подтверждения почты возвращаются JWT токены для авторизации, и ответ содержит статус 201 (Created).

    2. **Авторизация через JWT**:
       Если пользователь уже существует и его почта была ранее подтверждена, он может ввести 6-значный код для авторизации и получения новых JWT токенов (refresh и access). В этом случае возвращается статус 200 (OK).

    Процесс:
    - Пользователь вводит email и код, система проверяет корректность кода и его срок действия.
    - Если код действителен и email не был подтверждён ранее, возвращается статус 201 (Created) и токены.
    - Если email уже был подтверждён, возвращается статус 200 (OK) и токены для доступа.

    Возможные ошибки:
    - 404: Пользователь с таким email не найден.
    - 400: Неверный код подтверждения или срок действия кода истёк.

    После успешного подтверждения или авторизации возвращаются данные пользователя и токены для доступа.
    """

    serializer_class = VerifyEmailCodeSerializer

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailCodeSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise ValidationError(
                {"detail": "User not found."}, code=status.HTTP_404_NOT_FOUND
            )

        try:
            verification_code = EmailVerificationCode.objects.get(
                user=user, code=code, is_used=False
            )
        except EmailVerificationCode.DoesNotExist:
            raise ValidationError(
                {"detail": "Invalid confirmation code."},
                code=status.HTTP_400_BAD_REQUEST,
            )

        if verification_code.is_expired():
            raise ValidationError(
                {"detail": "The confirmation code has expired."},
                code=status.HTTP_400_BAD_REQUEST,
            )

        verification_code.is_used = True
        verification_code.save()
        email_confirmation = EmailAddress.objects.get(user=user, email=user.email)
        if not email_confirmation.verified:
            email_confirmation.verified = True
            email_confirmation.save()
            status_code = status.HTTP_201_CREATED
        else:
            status_code = status.HTTP_200_OK

        user.save()
        tokens = self.generate_token(user)
        user_data = UserSerializer(user).data
        response_data = {"user": user_data, "tokens": tokens}
        return Response(response_data, status=status_code)

    def generate_token(self, user):
        refresh = RefreshToken.for_user(user)
        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


@extend_schema(tags=["User Management"])
class PasswordResetView(APIView):
    serializer_class = PasswordResetSerializer
    permission_classes = [AllowAny]

    @extend_schema(summary="Сброс пароля")
    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            try:
                user = User.objects.get(email=email)
                token = default_token_generator.make_token(user)
                reset_url = request.build_absolute_uri(
                    reverse("password-reset-confirm", args=[user.pk, token])
                )
                send_email(
                    "Password Reset",
                    f"Click the link to reset your password: {reset_url}",
                    settings.DEFAULT_FROM_EMAIL,
                    [email],
                )
                return Response(
                    {"message": "Password reset link sent"}, status=status.HTTP_200_OK
                )
            except User.DoesNotExist:
                return Response(
                    {"error": "User with this email does not exist"},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["User Management"])
class PasswordResetConfirmView(APIView):
    serializer_class = PasswordResetConfirmSerializer
    permission_classes = [AllowAny]

    @extend_schema(summary="Подтверждение сброса пароля")
    def post(self, request, user_id, token, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            try:
                user = User.objects.get(pk=user_id)
                if default_token_generator.check_token(user, token):
                    user.set_password(serializer.validated_data["new_password"])
                    user.save()
                    return Response(
                        {"message": "Password reset successfully"},
                        status=status.HTTP_200_OK,
                    )
                else:
                    return Response(
                        {"error": "Invalid token"}, status=status.HTTP_400_BAD_REQUEST
                    )
            except User.DoesNotExist:
                return Response(
                    {"error": "Invalid user"}, status=status.HTTP_400_BAD_REQUEST
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(
    tags=["Authentication"],
    request=LogoutSerializer,
    summary="Выход пользователя",
    responses={
        status.HTTP_200_OK: OpenApiResponse(
            response=dict,
            description="Успешная деактивация токена",
            examples=[
                OpenApiExample(
                    name="Деактивация токена",
                    summary="Токен успешно деактивирован",
                    value={"status": "OK, goodbye"},
                ),
                OpenApiExample(
                    name="Деактивация всех токенов",
                    summary="Все refresh токены деактивированы",
                    value={"status": "OK, goodbye, all refresh tokens blacklisted"},
                ),
            ],
        ),
        status.HTTP_400_BAD_REQUEST: OpenApiResponse(
            response=dict,
            description="Ошибка при деактивации токена",
            examples=[
                OpenApiExample(
                    name="Ошибка при деактивации",
                    summary="Ошибка при деактивации токена",
                    value={"status": "error"},
                ),
                OpenApiExample(
                    name="Токен не передан",
                    summary="Не передан refresh токен",
                    value={"status": "error", "detail": "refresh_token is required"},
                ),
                OpenApiExample(
                    name="Токен не найден",
                    summary="Не найдено токенов для пользователя",
                    value={"status": "error", "detail": "No tokens found for user"},
                ),
                OpenApiExample(
                    name="Неверный токен",
                    summary="Неверный токен",
                    value={"status": "error", "detail": "Invalid token"},
                ),
            ],
        ),
        status.HTTP_401_UNAUTHORIZED: OpenApiResponse(
            response=dict,
            description="Токен доступа не предоставлен",
            examples=[
                OpenApiExample(
                    name="Токен не предоставлен",
                    summary="Токен доступа не предоставлен",
                    value={"detail": "Authentication credentials were not provided."},
                ),
            ],
        ),
    },
)
class APILogoutView(APIView):
    """
    API для выхода пользователя

    Этот эндпоинт позволяет авторизованному пользователю выйти из системы и деактивировать его refresh токены.

    В зависимости от переданных параметров, API позволяет деактивировать один конкретный refresh токен или все токены пользователя.

    Разрешения:
    - Доступ имеют только авторизованные пользователи (требуется `Bearer` токен).

    Метод: POST

    Запрос:
    - Заголовки:
        - Authorization: Bearer <access_token>
    - Тело запроса:
        - refresh_token (строка, обязательно): Refresh токен, который нужно деактивировать.
        - all_tokens (булево, опционально): Если true, будут деактивированы все refresh токены пользователя.

    Примеры запросов:
    1. **Деактивация одного токена**:
    ```json
    {
        "refresh_token": "your_refresh_token_here"
    }
    ```

    2. **Деактивация всех токенов пользователя**:
    ```json
    {
        "all_tokens": true
    }
    ```

    Ответы:
    - 200 OK:
        - {"status": "OK, goodbye"}: Успешная деактивация указанного refresh токена.
        - {"status": "OK, goodbye, all tokens blacklisted"}: Успешная деактивация всех refresh токенов пользователя.
    - 400 Bad Request:
        - {"status": "error", "detail": "refresh_token is required"}: Если refresh_token не был передан.
        - {"status": "error", "detail": "No tokens found for user"}: Если у пользователя не найдено ни одного токена для деактивации.
        - {"status": "error", "detail": "Invalid token"}: Если переданный токен недействителен.
    - 401 Unauthorized:
        - {"detail": "Authentication credentials were not provided."}: Токен доступа не был предоставлен или недействителен.
    """

    permission_classes = [IsAuthenticated]
    serializer_class = LogoutSerializer

    @extend_schema(summary="Выход пользователя")
    def post(self, request, *args, **kwargs):
        try:
            if self.request.data.get("all_tokens", False):
                tokens = OutstandingToken.objects.filter(user=request.user)
                if not tokens.exists():
                    return Response(
                        {"status": "error", "detail": "No tokens found for user."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                for token in tokens:
                    BlacklistedToken.objects.get_or_create(token=token)
                return Response(
                    {"status": "OK, all tokens blacklisted"}, status=status.HTTP_200_OK
                )

            refresh_token = request.data.get("refresh_token", None)
            print(refresh_token)
            print(request.data)
            if not refresh_token:
                return Response(
                    {"status": "error", "detail": "refresh_token is required."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                return Response(
                    {"status": "error", "detail": str(e)},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            return Response(
                {"status": "OK, token blacklisted"}, status=status.HTTP_200_OK
            )
        except Exception:
            return Response({"status": "error"}, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=["Authentication"], summary="Обновление токена")
class CustomTokenRefreshView(TokenRefreshView):
    """ 
    Принимает refresh токен и возвращает новый access токен, \
        если refresh токен действителен.
    """

    pass


@extend_schema(tags=["Authentication"], summary="Проверка токена")
class CustomTokenVerifyView(TokenVerifyView):
    """ 
    Принимает access токен и возвращает пустой ответ, \
        если токен действителен."""

    pass

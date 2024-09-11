from rest_framework import permissions
import logging

logger = logging.getLogger(__name__)


class AdminFullAccessAuthenticatedReadOnly(permissions.BasePermission):
    """
    Разрешения:
    - Все действия доступны администратору.
    - Только просмотр доступен аутентифицированным пользователям.
    - 403 Forbidden для неаутентифицированных.
    """

    def has_permission(self, request, view):
        return True
        try:
            if DEBUG:
                return True
            # Разрешить все действия администратору
            if request.user and request.user.is_staff:
                logger.info(
                    "Доступ предоставлен администратору", extra={"request": request}
                )
                return True

            # Разрешить только просмотр для аутентифицированных пользователей
            if (
                request.method in permissions.SAFE_METHODS
                and request.user.is_authenticated
            ):
                logger.info(
                    "Доступ предоставлен аутентифицированному пользователю",
                    extra={"request": request},
                )
                return True

            # Запретить доступ неаутентифицированным пользователям
            logger.warning(
                "Доступ запрещен неаутентифицированному пользователю",
                extra={"request": request},
            )
            return False
        except Exception as e:
            logger.error(
                f"Ошибка в проверке разрешений: {str(e)}", extra={"request": request}
            )
            return False


from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status


class CustomIsAuthenticated(BasePermission):

    def has_permission(self, request, view):
        # Проверка аутентификации пользователя
        if not request.user or not request.user.is_authenticated:
            raise AuthenticationFailed(
                "Authentication credentials were not provided or are invalid."
            )

        # Если пользователь аутентифицирован, возвращаем True
        return True

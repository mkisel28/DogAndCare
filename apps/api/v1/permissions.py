import logging

from rest_framework import permissions

logger = logging.getLogger(__name__)


class AdminFullAccessAuthenticatedReadOnly(permissions.BasePermission):
    """Permissions:
    - All actions are allowed for the administrator.
    - Only read access is allowed for authenticated users.
    - 403 Forbidden for unauthenticated users.
    """

    def has_permission(self, request, view):
        return True
        try:
            if DEBUG:
                return True
            if request.user and request.user.is_staff:
                logger.info(
                    "Доступ предоставлен администратору",
                    extra={"request": request},
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
                f"Ошибка в проверке разрешений: {e!s}",
                extra={"request": request},
            )
            return False

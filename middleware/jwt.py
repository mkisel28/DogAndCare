from dj_rest_auth.jwt_auth import JWTCookieAuthentication
from django.utils.deprecation import MiddlewareMixin
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


class JWTUserMiddleware(MiddlewareMixin):
    def process_request(self, request):
        jwt_authenticator = JWTCookieAuthentication()
        try:
            user_auth_tuple = jwt_authenticator.authenticate(request)
            if user_auth_tuple is not None:
                request.user, _ = user_auth_tuple
        except (InvalidToken, TokenError, AuthenticationFailed):
            pass

        except Exception as exc:
            response = Response(
                {
                    "status": "error",
                    "detail": "Unknown Error",
                    "code": "unknown_error",
                    "messages": [{"message": str(exc)}],
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

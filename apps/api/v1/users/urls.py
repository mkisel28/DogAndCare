from django.urls import path


from apps.api.v1.users.views.views import (
    ConfirmDeleteUserView,
    CurrentUserView,
    RequestDeleteUserView,
)

urlpatterns = [
    path("", CurrentUserView.as_view(), name="user"),
    path(
        "delete/request/", RequestDeleteUserView.as_view(), name="request-delete-user"
    ),
    path(
        "delete/confirm/", ConfirmDeleteUserView.as_view(), name="confirm-delete-user"
    ),
]

from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("apps.api.urls")),
]

from django.conf import settings

if "debug_toolbar" in settings.INSTALLED_APPS:

    urlpatterns += [
        path("__debug__/", include("debug_toolbar.urls")),
    ]

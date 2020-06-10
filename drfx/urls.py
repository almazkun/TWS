from django.contrib import admin
from django.urls import include, path
from django.conf.urls.static import static


urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include("api.urls")),
    path("api-auth/", include("rest_framework.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
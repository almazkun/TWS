from django.urls import include, path
from .views import validate_IIN


urlpatterns = [
    path("", validate_IIN),
    path("rest-auth/", include("rest_auth.urls")),
    path("rest-auth/registration/", include("rest_auth.registration.urls")),
    path("users/", include("users.urls")),
]

from django.urls import include, path
from django.contrib import admin
from .admin import superuser_admin_site

urlpatterns = [
	path("admin/", superuser_admin_site.urls),
	path("", include("profiles.urls", namespace="profiles")),
]



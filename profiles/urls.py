"""
URL configuration for the profiles application.

This module defines URL patterns for profile viewing, editing, map visualization,
and the GeoJSON API endpoint. All URLs are namespaced under 'profiles'.

URL Patterns:
	/ - Home page (public)
	/me/ - Current user's profile (authenticated)
	/me/edit/ - Edit current user's profile (authenticated)
	/map/ - Interactive map of all users (public)
	/api/users-geojson/ - GeoJSON API endpoint (authenticated)
"""
from django.urls import path

from . import views

app_name = "profiles"

urlpatterns = [
	path("", views.HomeView.as_view(), name="home"),
	path("me/", views.MyProfileView.as_view(), name="my_profile"),
	path("me/edit/", views.EditMyProfileView.as_view(), name="edit_my_profile"),
	path("map/", views.UsersMapView.as_view(), name="users_map"),
	path("api/users-geojson/", views.users_geojson, name="users_geojson"),
]



"""
Django admin configuration for profiles app models.

This module registers the Profile and LoginActivity models with the Django
admin interface, providing customized list displays, search, and filtering
capabilities. Profile admin uses LeafletGeoAdmin for map-based location editing.
"""
from django.contrib import admin
from leaflet.admin import LeafletGeoAdmin

from .models import Profile, LoginActivity


@admin.register(Profile)
class ProfileAdmin(LeafletGeoAdmin):
	"""
	Admin interface for Profile model with Leaflet map widget.
	
	Provides a list view with user, address, and phone fields, and enables
	searching by username, address, or phone number. Uses LeafletGeoAdmin
	to display an interactive map for editing the location field.
	"""
	list_display = ("user", "home_address", "phone_number")
	search_fields = ("user__username", "home_address", "phone_number")


@admin.register(LoginActivity)
class LoginActivityAdmin(admin.ModelAdmin):
	"""
	Admin interface for LoginActivity model.
	
	Displays login/logout events with user, action type, timestamp, and IP address.
	Provides filtering by action type and timestamp, and search by username,
	IP address, or user agent string.
	"""
	list_display = ("user", "action", "timestamp", "ip_address")
	list_filter = ("action", "timestamp")
	search_fields = ("user__username", "ip_address", "user_agent")



"""
Models for user profiles and login activity tracking.

This module defines the Profile model which extends Django's User model with
additional fields including geospatial location data, and the LoginActivity
model for tracking user authentication events.
"""
from django.conf import settings
from django.contrib.gis.db import models as gis_models
from django.db import models
from django.utils import timezone


class Profile(models.Model):
	"""
	Extended user profile with address, phone, and geographic location.
	
	This model has a one-to-one relationship with Django's User model and stores
	additional profile information including a PostGIS Point geometry for the
	user's location.
	
	Attributes:
		user: OneToOne relationship to Django User model
		home_address: User's home address (optional)
		phone_number: User's phone number (optional)
		location: Geographic point using PostGIS PointField with geography=True
		          for accurate distance calculations on Earth's surface
		created_at: Timestamp when profile was created
		updated_at: Timestamp when profile was last updated
	"""
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="profile")
	home_address = models.CharField(max_length=255, blank=True)
	phone_number = models.CharField(max_length=32, blank=True)
	location = gis_models.PointField(geography=True, null=True, blank=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ["user__username"]

	def __str__(self):
		return f"Profile({self.user.username})"


class LoginActivity(models.Model):
	"""
	Track user login and logout events for auditing and monitoring.
	
	This model records authentication events including the action type (login/logout),
	timestamp, IP address, and user agent string for security and analytics purposes.
	
	Attributes:
		user: Foreign key to Django User model
		action: Type of action - either 'login' or 'logout'
		timestamp: When the action occurred
		ip_address: IP address of the user (supports IPv4 and IPv6)
		user_agent: Browser user agent string
	"""
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="login_activities")
	action = models.CharField(max_length=16, choices=(("login", "login"), ("logout", "logout")))
	timestamp = models.DateTimeField(default=timezone.now)
	ip_address = models.GenericIPAddressField(null=True, blank=True)
	user_agent = models.TextField(blank=True)

	class Meta:
		ordering = ["-timestamp"]

	def __str__(self):
		return f"{self.user} {self.action} at {self.timestamp:%Y-%m-%d %H:%M:%S}"



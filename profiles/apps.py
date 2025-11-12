"""
Application configuration for the profiles app.

This module configures the profiles application and registers signal handlers
for automatic profile creation and login activity tracking.
"""
from django.apps import AppConfig


class ProfilesConfig(AppConfig):
	"""
	Configuration class for the profiles application.
	
	Registers signal handlers when the app is ready to ensure automatic
	profile creation and login/logout activity logging.
	"""
	default_auto_field = "django.db.models.BigAutoField"
	name = "profiles"

	def ready(self):
		"""
		Import signal handlers when the application is ready.
		
		This ensures that signal handlers are registered and active
		for automatic profile creation and activity logging.
		"""
		from . import signals  # noqa: F401



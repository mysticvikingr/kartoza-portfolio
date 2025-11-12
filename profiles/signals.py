"""
Signal handlers for automatic profile creation and login activity tracking.

This module uses Django signals to automatically create user profiles when
new users are created and to log all login/logout events for auditing purposes.
"""
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile, LoginActivity

User = get_user_model()


@receiver(post_save, sender=User)
def create_profile_for_user(sender, instance, created, **kwargs):
	"""
	Automatically create a Profile when a new User is created.
	
	This signal handler ensures every user has an associated profile
	without requiring manual creation. Uses get_or_create to prevent
	duplicate profiles if called multiple times.
	
	Args:
		sender: The User model class
		instance: The User instance being saved
		created: Boolean indicating if this is a new user
		**kwargs: Additional signal arguments
	"""
	if created:
		Profile.objects.get_or_create(user=instance)


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
	"""
	Log user login events with IP address and user agent.
	
	Creates a LoginActivity record whenever a user successfully logs in.
	Captures the IP address and browser user agent for security auditing.
	
	Args:
		sender: The signal sender
		request: HTTP request object containing META data
		user: The User instance that logged in
		**kwargs: Additional signal arguments
	"""
	ip = None
	if request and hasattr(request, "META"):
		ip = request.META.get("REMOTE_ADDR")
	ua = request.META.get("HTTP_USER_AGENT", "") if request else ""
	LoginActivity.objects.create(user=user, action="login", ip_address=ip, user_agent=ua)


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
	"""
	Log user logout events with IP address and user agent.
	
	Creates a LoginActivity record whenever a user logs out.
	Captures the IP address and browser user agent for security auditing.
	
	Args:
		sender: The signal sender
		request: HTTP request object containing META data
		user: The User instance that logged out
		**kwargs: Additional signal arguments
	"""
	ip = None
	if request and hasattr(request, "META"):
		ip = request.META.get("REMOTE_ADDR")
	ua = request.META.get("HTTP_USER_AGENT", "") if request else ""
	LoginActivity.objects.create(user=user, action="logout", ip_address=ip, user_agent=ua)



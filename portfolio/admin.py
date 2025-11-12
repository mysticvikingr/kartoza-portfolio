"""
Custom Django admin site with superuser-only access.

This module creates a custom admin site that restricts access to superusers only,
providing an additional layer of security beyond Django's default admin permissions.
Normal authenticated users cannot access the admin interface at all.
"""
from django.contrib.admin import AdminSite
from django.contrib import admin


class SuperuserOnlyAdminSite(AdminSite):
	"""
	Custom admin site that only allows superuser access.
	
	Overrides the default Django admin site to enforce superuser-only access.
	This ensures that normal users cannot access any admin functionality,
	even if they have staff status or specific model permissions.
	
	Attributes:
		site_header: Header text displayed in admin interface
		site_title: Browser title for admin pages
		index_title: Title on admin index page
	"""
	site_header = "Portfolio Admin"
	site_title = "Portfolio Admin"
	index_title = "Administration"

	def has_permission(self, request):
		"""
		Check if user has permission to access the admin site.
		
		Only active superusers are granted access. This overrides Django's
		default behavior which allows any staff user to access admin.
		
		Args:
			request: HTTP request object with user information
			
		Returns:
			bool: True if user is an active superuser, False otherwise
		"""
		return bool(request.user and request.user.is_active and request.user.is_superuser)


# Create instance of custom admin site
superuser_admin_site = SuperuserOnlyAdminSite(name="superuser_admin")

# Re-register all models from default admin site to custom admin site
# This ensures all registered models are available in the superuser-only admin
for model, model_admin in admin.site._registry.items():
	superuser_admin_site.register(model, model_admin.__class__)



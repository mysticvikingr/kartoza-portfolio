"""
Views for user profile management and map visualization.

This module contains views for displaying and editing user profiles,
showing an interactive map of all users, and providing a GeoJSON API
endpoint with role-based access control.
"""
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import TemplateView
from django.contrib.gis.geos import Point

from .forms import ProfileForm
from .models import Profile


class HomeView(TemplateView):
	"""
	Public home page view.
	
	Displays welcome message and overview of application features.
	No authentication required.
	"""
	template_name = "profiles/home.html"


class MyProfileView(LoginRequiredMixin, TemplateView):
	"""
	Display the current user's profile.
	
	Requires authentication. Automatically creates a profile if one doesn't
	exist for the user. Users can only view their own profile.
	"""
	template_name = "profiles/my_profile.html"

	def get_context_data(self, **kwargs):
		"""Add user's profile to template context."""
		ctx = super().get_context_data(**kwargs)
		profile, _ = Profile.objects.get_or_create(user=self.request.user)
		ctx["profile"] = profile
		return ctx


class EditMyProfileView(LoginRequiredMixin, View):
	"""
	Handle profile editing for the current user.
	
	GET: Display form with current profile data, extracting lat/lng from Point geometry
	POST: Validate and save profile data, constructing Point from lat/lng inputs
	
	Requires authentication. Users can only edit their own profile.
	"""
	template_name = "profiles/edit_my_profile.html"
	success_url = reverse_lazy("profiles:my_profile")

	def get(self, request: HttpRequest):
		"""Display profile edit form with current data."""
		profile, _ = Profile.objects.get_or_create(user=request.user)
		initial = {}
		# Extract latitude and longitude from Point geometry for form display
		if profile.location:
			initial["latitude"] = profile.location.y
			initial["longitude"] = profile.location.x
		form = ProfileForm(instance=profile, initial=initial)
		return render(request, self.template_name, {"form": form})

	def post(self, request: HttpRequest):
		"""Process profile update form submission."""
		profile, _ = Profile.objects.get_or_create(user=request.user)
		form = ProfileForm(request.POST, instance=profile)
		if form.is_valid():
			obj = form.save(commit=False)
			# Construct Point geometry from latitude and longitude inputs
			lat = form.cleaned_data.get("latitude")
			lng = form.cleaned_data.get("longitude")
			if lat is not None and lng is not None:
				obj.location = Point(lng, lat)  # Note: Point(x=lng, y=lat)
			obj.save()
			messages.success(request, "Profile updated.")
			return redirect(self.success_url)
		return render(request, self.template_name, {"form": form})


class UsersMapView(TemplateView):
	"""
	Display full-screen interactive map showing all user locations.
	
	Public view (no authentication required). Fetches user data via AJAX
	from the GeoJSON endpoint which handles role-based filtering.
	"""
	template_name = "profiles/users_map.html"


@login_required
def users_geojson(request: HttpRequest):
	"""
	Return GeoJSON FeatureCollection of all users with locations.
	
	Implements role-based access control:
	- Normal users: See only usernames for other users
	- Superusers: See full details (username, address, phone) for all users
	- All users: See profile URL only for their own marker
	
	Args:
		request: HTTP request object with authenticated user
		
	Returns:
		JsonResponse containing GeoJSON FeatureCollection with Point geometries
		and filtered properties based on user role
	"""
	# Query all profiles with locations, optimize with select_related
	qs = Profile.objects.select_related("user").exclude(location__isnull=True)
	features = []
	
	for p in qs:
		point = p.location
		# Filter properties based on user role
		props = {
			"username": p.user.username,
			"home_address": p.home_address if request.user.is_superuser else "",
			"phone_number": p.phone_number if request.user.is_superuser else "",
			"profile_url": reverse_lazy("profiles:my_profile")
				if request.user == p.user
				else "",
		}
		features.append(
			{
				"type": "Feature",
				"geometry": {"type": "Point", "coordinates": [point.x, point.y]},
				"properties": props,
			}
		)
	return JsonResponse({"type": "FeatureCollection", "features": features})



"""
Forms for user profile editing with geospatial input.

This module provides a ModelForm for Profile editing that includes
a Leaflet map widget for visual location selection and separate
latitude/longitude fields for numeric input.
"""
from django import forms
from django.contrib.gis.geos import Point
from leaflet.forms.widgets import LeafletWidget

from .models import Profile


class ProfileForm(forms.ModelForm):
	"""
	Form for editing user profile with geographic location.
	
	Provides multiple ways to input location:
	1. Visual selection via Leaflet map widget
	2. Manual entry of latitude and longitude coordinates
	
	The form automatically constructs a PostGIS Point geometry from
	the latitude and longitude inputs during validation.
	
	Fields:
		home_address: Text input for user's address
		phone_number: Text input for user's phone
		location: Hidden field with Leaflet map widget for visual selection
		latitude: Numeric input for latitude coordinate
		longitude: Numeric input for longitude coordinate
	"""
	latitude = forms.FloatField(required=False, help_text="Latitude coordinate (Y)")
	longitude = forms.FloatField(required=False, help_text="Longitude coordinate (X)")

	class Meta:
		model = Profile
		fields = ["home_address", "phone_number", "location"]
		widgets = {"location": LeafletWidget()}

	def clean(self):
		"""
		Validate form data and construct Point geometry from lat/lng.
		
		If latitude and longitude are provided but no location Point exists,
		this method constructs a Point geometry with the coordinates.
		Note: PostGIS Point uses (longitude, latitude) order (X, Y).
		
		Returns:
			dict: Cleaned form data with constructed Point geometry if applicable
		"""
		cleaned = super().clean()
		lat = self.cleaned_data.get("latitude")
		lng = self.cleaned_data.get("longitude")
		loc = self.cleaned_data.get("location")
		
		# Construct Point from lat/lng if both provided and no existing location
		if (lat is not None and lng is not None) and not loc:
			cleaned["location"] = Point(lng, lat)  # Point(x=longitude, y=latitude)
		return cleaned



from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.gis.geos import Point

from .models import Profile


class ProfileTests(TestCase):
	def setUp(self):
		User = get_user_model()
		self.user = User.objects.create_user(username="alice", password="pass12345")
		self.superuser = User.objects.create_superuser(username="admin", password="pass12345")

	def test_profile_auto_created(self):
		self.assertTrue(Profile.objects.filter(user=self.user).exists())

	def test_my_profile_requires_login(self):
		resp = self.client.get(reverse("profiles:my_profile"))
		self.assertEqual(resp.status_code, 302)  # redirect to login

	def test_user_sees_own_profile(self):
		c = Client()
		self.assertTrue(c.login(username="alice", password="pass12345"))
		resp = c.get(reverse("profiles:my_profile"))
		self.assertEqual(resp.status_code, 200)
		self.assertContains(resp, "My Profile")

	def test_edit_profile_sets_point(self):
		c = Client()
		c.login(username="alice", password="pass12345")
		resp = c.post(
			reverse("profiles:edit_my_profile"),
			{
				"home_address": "123 Main St",
				"phone_number": "123456",
				"latitude": 10,
				"longitude": 20,
			},
			follow=True,
		)
		self.assertEqual(resp.status_code, 200)
		p = Profile.objects.get(user=self.user)
		self.assertIsNotNone(p.location)
		self.assertAlmostEqual(p.location.x, 20)
		self.assertAlmostEqual(p.location.y, 10)

	def test_users_geojson_hides_sensitive_for_normal_user(self):
		p = self.user.profile
		p.location = Point(1, 2)
		p.home_address = "secret"
		p.phone_number = "secret"
		p.save()
		c = Client()
		c.login(username="alice", password="pass12345")
		resp = c.get(reverse("profiles:users_geojson"))
		self.assertEqual(resp.status_code, 200)
		data = resp.json()
		props = data["features"][0]["properties"]
		self.assertEqual(props["home_address"], "")
		self.assertEqual(props["phone_number"], "")

	def test_users_geojson_shows_sensitive_for_superuser(self):
		p = self.user.profile
		p.location = Point(1, 2)
		p.home_address = "secret"
		p.phone_number = "secret"
		p.save()
		c = Client()
		c.login(username="admin", password="pass12345")
		resp = c.get(reverse("profiles:users_geojson"))
		props = resp.json()["features"][0]["properties"]
		self.assertEqual(props["home_address"], "secret")
		self.assertEqual(props["phone_number"], "secret")



from django.test import TestCase, Client
from django.contrib.admin.sites import site
from django.urls import reverse
from django.contrib.auth import get_user_model
from restourant.models import Dish


class AdminSiteTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.admin_user = get_user_model().objects.create_superuser(
            username="admin",
            password="password123"
        )
        self.client.login(username="admin", password="password123")

        self.cook = get_user_model().objects.create_user(
            username="simple_cook",
            password="password123",
            years_of_experience=5
        )

    def test_cook_years_of_experience_listed(self):
        url = reverse("admin:restourant_cook_changelist")
        response = self.client.get(url)

        self.assertContains(response, "years_of_experience")
        self.assertContains(response, "5")

    def test_cook_detail_page_has_additional_fields(self):
        url = reverse("admin:restourant_cook_change", args=[self.cook.id])
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "years_of_experience")

    def test_model_registered_in_admin(self):
        models_in_admin = [model for model, model_admin in site._registry.items()]
        self.assertIn(Dish, models_in_admin)

    def test_regular_user_cannot_access_admin(self):
        self.client.logout()

        self.client.login(username="simple_cook", password="password123")

        url = reverse("admin:index")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 302)

    def test_dish_admin_search(self):
        from restourant.models import DishType
        dt = DishType.objects.create(name="Soup")
        Dish.objects.create(name="UniqueDishName", price=10, dish_type=dt)

        url = reverse("admin:restourant_dish_changelist")
        response = self.client.get(url, {'q': 'UniqueDishName'})

        self.assertContains(response, "UniqueDishName")

from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from restourant.models import Dish, DishType, Ingredient


class ViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="test_admin",
            password="password123"
        )
        self.client.login(username="test_admin", password="password123")

        self.dish_type = DishType.objects.create(name="Супи")

        self.ingredient = Ingredient.objects.create(name="Сіль")

        self.dish = Dish.objects.create(
            name="Борщ",
            price=120,
            dish_type=self.dish_type
        )
        self.dish.ingredients.add(self.ingredient, through_defaults={})
        self.dish.cooks.add(self.user)

    def test_dish_list_view(self):
        response = self.client.get(reverse("restourant:dish-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "restourant/dish_list.html")
        self.assertContains(response, "Борщ")
        self.assertIn("dish_list", response.context)

    def test_cook_list_view(self):
        response = self.client.get(reverse("restourant:cook-list"))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "restourant/cook_list.html")
        self.assertContains(response, "test_admin")

    def test_dish_detail_view(self):
        response = self.client.get(
            reverse("restourant:dish-detail", kwargs={"pk": self.dish.id})
        )

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "restourant/dish_detail.html")
        self.assertContains(response, "Борщ")
        self.assertEqual(response.context["dish"], self.dish)

    def test_login_required_for_dish_list(self):
        self.client.logout()
        url = reverse("restourant:dish-list")
        response = self.client.get(url)
        login_url = reverse("login")
        self.assertRedirects(response, f"{login_url}?next={url}")

    def test_ingredient_create_view(self):
        from restourant.models import Ingredient

        response = self.client.post(
            reverse("restourant:ingredient-create"),
            data={"name": "Олія соняшникова"}
        )
        if response.status_code == 200:
            print(response.context["form"].errors)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Ingredient.objects.filter(name="Сіль").exists())

    def test_dish_update_view(self):
        new_ingredient = Ingredient.objects.create(name="Часник")

        url = reverse("restourant:dish-update", kwargs={"pk": self.dish.id})
        data = {
            "name": "Борщ оновлений",
            "price": 350,
            "dish_type": self.dish_type.id,
            "description": "Новий опис",
            "cooks": [self.user.id],
            "ingredients": [self.ingredient.id, new_ingredient.id]
        }

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, 302)
        self.dish.refresh_from_db()
        self.assertEqual(self.dish.name, "Борщ оновлений")

    def test_ingredient_delete_view(self):
        """Перевірка видалення інгредієнта"""
        ingredient = Ingredient.objects.create(name="Видалити мене")
        url = reverse("restourant:ingredient-delete", kwargs={"pk": ingredient.id})
        response = self.client.post(url)

        self.assertEqual(response.status_code, 302)
        self.assertFalse(Ingredient.objects.filter(id=ingredient.id).exists())

    def test_dish_pagination_is_six(self):
        for i in range(10):
            Dish.objects.create(
                name=f"Страва {i}",
                price=100 + i,
                dish_type=self.dish_type
            )

        response = self.client.get(reverse("restourant:dish-list"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["is_paginated"])
        self.assertEqual(len(response.context["dish_list"]), 6)

    def test_dish_list_contains_search_form(self):
        response = self.client.get(reverse("restourant:dish-list"))
        self.assertIn("search_form", response.context)
        from restourant.forms import DishSearchForm
        self.assertIsInstance(response.context["search_form"], DishSearchForm)

from django.contrib.auth import get_user_model
from django.test import TestCase
from restourant.forms import CookExperienceUpdateForm, DishForm
from restourant.models import Ingredient, DishType


class CookFormsTests(TestCase):
    def setUp(self):
        self.dish_type = DishType.objects.create(name="Супи")

        self.ingredient = Ingredient.objects.create(name="Сіль")

        self.user = get_user_model().objects.create_user(
            username="test_cook",
            password="password123"
        )

    def test_cook_experience_update_form_valid_data(self):
        form_data = {"years_of_experience": 10}
        form = CookExperienceUpdateForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_cook_experience_update_form_invalid_data(self):
        form_data = {"years_of_experience": -1}
        form = CookExperienceUpdateForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)

    def test_dish_form_many_to_many_validation(self):
        form_data = {
            "name": "Борщ",
            "price": 150,
            "dish_type": self.dish_type.id,
            "ingredients": [],  # Порожній список інгредієнтів
        }
        form = DishForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("ingredients", form.errors)

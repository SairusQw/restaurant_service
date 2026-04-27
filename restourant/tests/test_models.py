from django.test import TestCase
from django.contrib.auth import get_user_model
from restourant.models import Dish, DishType, Ingredient


class ModelTests(TestCase):

    def setUp(self):
        self.dish_type = DishType.objects.create(
            name="Десерти"
        )
        self.ingredient = Ingredient.objects.create(
            name="Цукор"
        )
        self.cook = get_user_model().objects.create_user(
            username="test_chef",
            password="password123",
            years_of_experience=5
        )

    def test_dish_type_str(self):
        self.assertEqual(str(self.dish_type), "Десерти")

    def test_ingredient_str(self):
        self.assertEqual(str(self.ingredient), "Цукор")

    def test_cook_str(self):
        expected_str = f"{self.cook.username} ({self.cook.years_of_experience} years of experience)"
        self.assertEqual(str(self.cook), expected_str)

    def test_dish_creation_and_str(self):
        dish = Dish.objects.create(
            name="Тірамісу",
            price=150,
            dish_type=self.dish_type
        )
        dish.cooks.add(self.cook)

        self.assertEqual(dish.name, "Тірамісу")
        self.assertEqual(str(dish), "Тірамісу")
        self.assertIn(self.cook, dish.cooks.all())
        self.assertEqual(dish.dish_type.name, "Десерти")

    def test_cook_experience_validation(self):
        self.assertEqual(self.cook.years_of_experience, 5)

    def test_create_cook_with_full_name(self):
        cook = get_user_model().objects.create_user(
            username="chef_pro",
            password="password123",
            first_name="Gordon",
            last_name="Ramsey"
        )
        self.assertEqual(cook.first_name, "Gordon")
        self.assertEqual(cook.last_name, "Ramsey")

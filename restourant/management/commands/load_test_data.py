import random
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from faker import Faker
from restourant.models import Dish, DishType, Ingredient

class Command(BaseCommand):
    help = "Populate database with sample English data for testing"

    def handle(self, *args, **kwargs):
        fake = Faker()
        self.stdout.write("Generating data...")

        categories = ["Pizza", "Pasta", "Burgers", "Salads", "Desserts", "Soups", "Steaks", "Seafood"]
        type_objs = []
        for name in categories:
            dt, _ = DishType.objects.get_or_create(name=name)
            type_objs.append(dt)

        ingredient_names = [
            "Cheese", "Tomato", "Chicken", "Beef", "Onion", "Garlic", "Bacon", "Mushrooms", 
            "Spinach", "Pepperoni", "Olive Oil", "Basil", "Shrimp", "Salmon", "Avocado"
        ]
        while len(ingredient_names) < 50:
            word = fake.word().capitalize()
            if word not in ingredient_names:
                ingredient_names.append(word)

        ing_objs = []
        for name in ingredient_names:
            ing, _ = Ingredient.objects.get_or_create(name=name)
            ing_objs.append(ing)

        cook_objs = []
        Cook = get_user_model()
        for _ in range(20):
            username = fake.user_name()
            if not Cook.objects.filter(username=username).exists():
                cook = Cook.objects.create_user(
                    username=username,
                    first_name=fake.first_name(),
                    last_name=fake.last_name(),
                    years_of_experience=random.randint(1, 25),
                    password="password123"
                )
                cook_objs.append(cook)

        base_names = ["Special", "Classic", "Hot", "Chef's", "Royal", "Garden", "Ocean"]
        for i in range(100):
            name = f"{random.choice(base_names)} {fake.word().capitalize()}"
            dish = Dish.objects.create(
                name=name,
                description=fake.paragraph(nb_sentences=3),
                price=random.randint(10, 100),
                dish_type=random.choice(type_objs)
            )
            dish.cooks.set(random.sample(cook_objs, k=random.randint(1, 3)))
            dish.ingredients.set(random.sample(ing_objs, k=random.randint(3, 8)))

        self.stdout.write(self.style.SUCCESS(f"Successfully populated 100 dishes and 20 cooks!"))
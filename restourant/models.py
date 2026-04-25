from django.contrib.auth.models import AbstractUser
from django.db import models

class DishType(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Dish(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=7, decimal_places=2)
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE,
                                  related_name="dishes")
    cooks = models.ManyToManyField("Cook", blank=True,
                                   related_name="dishes")
    ingredients = models.ManyToManyField("Ingredient",
                                         related_name="dishes",
                                         through="DishIngredient"
                                         )

    def __str__(self):
        return self.name


class Cook(AbstractUser):
    years_for_experience = models.IntegerField()

    class Meta:
        verbose_name = "cook"
        verbose_name_plural = "cooks"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"


class Ingredient(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class DishIngredient(models.Model):
    dish = models.ForeignKey(Dish, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    amount = models.CharField(max_length=50)

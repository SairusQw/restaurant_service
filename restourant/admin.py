from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from restourant.models import (DishType,
                               Ingredient,
                               DishIngredient,
                               Dish,
                               Cook)


@admin.register(DishType)
class DishTypeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)

# Налаштування inlines інгредієнтівб для того щоб додавати продукти у блюді
class DishIngredientInline(admin.TabularInline):
    model = DishIngredient
    extra = 1  # Кількість полів для нових інгрідієнтів

@admin.register(Dish)
class DishAdmin(admin.ModelAdmin):
    list_display = ("name", "price", "dish_type")
    list_filter = ("dish_type",)
    search_fields = ("name",)
    filter_horizontal = ("cooks",)
    inlines = [DishIngredientInline]

@admin.register(Cook)
class CookAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("years_of_experience",)
    fieldsets = UserAdmin.fieldsets + (
        ("Additional info", {"fields": ("years_of_experience",)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ("Additional info", {"fields": ("years_of_experience",)}),
    )

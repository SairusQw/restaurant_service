from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import generic

from restourant.models import (Cook,
                               Dish,
                               DishType,
                               Ingredient)


def index(request: HttpRequest) -> HttpResponse:
    num_cookies = Cook.objects.count()
    num_dishes = Dish.objects.count()
    top_cooks = Cook.objects.order_by("-years_of_experience")[:3]
    context = {
        "num_cookies": num_cookies,
        "num_dishes": num_dishes,
        "top_cooks": top_cooks,
    }
    return render(request, "restourant/index.html", context)


class DishTypeListView(generic.ListView):
    model = DishType
    template_name = "restourant/dish_type_list.html"
    context_object_name = "dish_type_list"

class DishListView(generic.ListView):
    model = Dish
    template_name = "restourant/dish_list.html"
    queryset = (Dish.objects.select_related("dish_type")
                .prefetch_related("cooks"))
    context_object_name = "dish_list"

class DishDetailView(generic.DetailView):
    model = Dish

class CookListView(generic.ListView):
    model = Cook
    template_name = "restourant/cook_list.html"

class CookDetailView(generic.DetailView):
    model = Cook

class IngredientListView(generic.ListView):
    model = Ingredient
    template_name = "restourant/ingredient_list.html"


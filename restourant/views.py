from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic

from restourant.forms import DishForm, CookExperienceUpdateForm, CookCreationForm, DishSearchForm, CookSearchForm, \
    IngredientSearchForm
from restourant.models import (Cook,
                               Dish,
                               DishType,
                               Ingredient)


def index(request: HttpRequest) -> HttpResponse:
    num_cooks = Cook.objects.count()
    num_dishes = Dish.objects.count()
    num_dish_types = DishType.objects.count()
    num_ingredients = Ingredient.objects.count()
    context = {
        "num_cooks": num_cooks,
        "num_dishes": num_dishes,
        "num_dish_types": num_dish_types,
        "num_ingredients": num_ingredients,
    }
    return render(request, "restourant/index.html", context)

class DishTypeListView(LoginRequiredMixin, generic.ListView):
    model = DishType
    fields = "__all__"
    paginate_by = 6
    template_name = "restourant/dish_type_list.html"
    context_object_name = "dish_type_list"

class DishTypeCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = DishType
    fields = "__all__"
    template_name = "restourant/dish_type_form.html"
    success_url = reverse_lazy("restourant:dish-type-list")
    success_message = "New category %(name)s created."

class DishTypeUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = DishType
    fields = "__all__"
    template_name = "restourant/dish_type_form.html"
    success_url = reverse_lazy("restourant:dish-type-list")
    success_message = "Category %(name)s successfully updated!"

class DishTypeDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = DishType
    template_name = "restourant/dish_type_confirm_delete.html"
    success_url = reverse_lazy("restourant:dish-type-list")

class DishListView(LoginRequiredMixin, generic.ListView):
    model = Dish
    template_name = "restourant/dish_list.html"
    paginate_by = 6
    queryset = (Dish.objects.select_related("dish_type")
                .prefetch_related("cooks"))
    context_object_name = "dish_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Передаємо форму в шаблон
        name = self.request.GET.get("name", "")
        context["search_form"] = DishSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        # Отримуємо назву з GET-запиту
        form = DishSearchForm(self.request.GET)
        queryset = Dish.objects.select_related("dish_type")

        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])

        return queryset

class DishDetailView(LoginRequiredMixin, generic.DetailView):
    model = Dish

class CookListView(LoginRequiredMixin, generic.ListView):
    model = Cook
    paginate_by = 8
    template_name = "restourant/cook_list.html"
    context_object_name = "cook_list"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = self.request.GET.get("username", "")
        context["search_form"] = CookSearchForm(initial={"username": username})
        return context

    def get_queryset(self):
        queryset = Cook.objects.all()
        form = CookSearchForm(self.request.GET)
        if form.is_valid():
            # Шукаємо одночасно по username та прізвищу
            query = form.cleaned_data["username"]
            return queryset.filter(
                Q(username__icontains=query) | Q(last_name__icontains=query)
            )
        return queryset

class DishCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Dish
    form_class = DishForm
    template_name = "restourant/dish_form.html"
    success_url = reverse_lazy("restourant:dish-list")
    success_message = "Dish %(name)s has been successfully created!"

class DishUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Dish
    form_class = DishForm
    template_name = "restourant/dish_form.html"
    success_url = reverse_lazy("restourant:dish-list")
    success_message = "Dish %(name)s has been successfully updated!"

class DishDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Dish
    template_name = "restourant/dish_confirm_delete.html"
    success_url = reverse_lazy("restourant:dish-list")

class CookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Cook

class CookCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Cook
    form_class = CookCreationForm
    template_name = "restourant/cook_form.html"
    success_url = reverse_lazy("restourant:cook-list")
    success_message = ("Welcome to the team!"
                       " Chef %(username)s has been successfully registered.")


class CookUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Cook
    form_class = CookExperienceUpdateForm
    template_name = "restourant/cook_form.html"
    success_url = reverse_lazy("restourant:cook-list")
    success_message = "Chef %(username)s has been successfully updated."

class CookDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Cook
    template_name = "restourant/cook_confirm_delete.html"
    success_url = reverse_lazy("restourant:cook-list")

class IngredientListView(LoginRequiredMixin, generic.ListView):
    model = Ingredient
    paginate_by = 6
    template_name = "restourant/ingredient_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        name = self.request.GET.get("name", "")
        context["search_form"] = IngredientSearchForm(initial={"name": name})
        return context

    def get_queryset(self):
        queryset = Ingredient.objects.all()
        form = IngredientSearchForm(self.request.GET)
        if form.is_valid():
            return queryset.filter(name__icontains=form.cleaned_data["name"])
        return queryset

class IngredientCreateView(LoginRequiredMixin, SuccessMessageMixin, generic.CreateView):
    model = Ingredient
    fields = "__all__"
    template_name = "restourant/ingredient_form.html"
    success_url = reverse_lazy("restourant:ingredient-list")
    success_message = "The ingredient %(name)s is now available for use in dishes."

class IngredientUpdateView(LoginRequiredMixin, SuccessMessageMixin, generic.UpdateView):
    model = Ingredient
    fields = "__all__"
    template_name = "restourant/ingredient_form.html"
    success_url = reverse_lazy("restourant:ingredient-list")
    success_message = "Ingredient %(name)s has been successfully updated."

class IngredientDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Ingredient
    template_name = "restourant/ingredient_confirm_delete.html"
    success_url = reverse_lazy("restourant:ingredient-list")



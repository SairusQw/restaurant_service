from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError

from .models import Dish, Cook, Ingredient


class DishForm(forms.ModelForm):
    ingredients = forms.ModelMultipleChoiceField(
        queryset=Ingredient.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True
    )
    cooks = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),
        required=False
    )

    class Meta:
        model = Dish
        fields = ["name", "description", "price", "dish_type", "cooks", "ingredients"]


class CookCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Cook
        fields = UserCreationForm.Meta.fields + (
            "first_name",
            "last_name",
            "years_of_experience",
        )

class CookExperienceUpdateForm(forms.ModelForm):
    class Meta:
        model = Cook
        fields = ["first_name", "last_name", "years_of_experience"]


class CookExperienceUpdateForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["years_of_experience"]

    def clean_years_of_experience(self):
        experience = self.cleaned_data.get("years_of_experience")

        if experience < 0:
            raise ValidationError("Стаж не може бути від’ємним!")
        if experience > 60:
            raise ValidationError("Стаж не може перевищувати 60 років!")

        return experience

class DishSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Search by name ..."
        })
    )

class CookSearchForm(forms.Form):
    username = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Search by username ..."
        })
    )

class IngredientSearchForm(forms.Form):
    name = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Search by name ..."
        })
    )

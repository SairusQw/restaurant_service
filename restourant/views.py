from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from restourant.models import Cook, Dish


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



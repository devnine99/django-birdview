from django.shortcuts import render
from django.views import View

from product.models import Ingredient


class HomeView(View):
    def get(self, request):
        ingredient_list = Ingredient.objects.all()
        return render(request, 'home.html', {'ingredient_list': ingredient_list})
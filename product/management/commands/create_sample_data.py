import json

from django.core.management import BaseCommand

from product.models import Product, Ingredient
from settings import PROJECT_DIR


class Command(BaseCommand):
    def handle(self, *args, **options):
        with open(PROJECT_DIR + '/product/fixtures/ingredients-data.json') as f:
            json_data = json.load(f)
        for ingredient in json_data:
            Ingredient.objects.create(**ingredient)

        with open(PROJECT_DIR + '/product/fixtures/products-data.json') as f:
            json_data = json.load(f)
        for product in json_data:
            ingredients = product.pop('ingredients').split(',')
            ingredient_list = Ingredient.objects.filter(name__in=ingredients)
            p = Product.objects.create(**product)
            p.ingredients.add(*ingredient_list)

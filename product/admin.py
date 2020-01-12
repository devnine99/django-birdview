from django.contrib import admin

from product.models import Product, Ingredient


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    pass

@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    pass

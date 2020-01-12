from rest_framework import serializers

from product.models import Product
from settings import IMAGE_URL


class ProductListSerializer(serializers.ModelSerializer):
    imgUrl = serializers.SerializerMethodField()
    ingredients = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'imgUrl', 'name', 'price', 'ingredients', 'monthlySales']

    def get_imgUrl(self, instance):
        return '{}/{}/{}'.format(IMAGE_URL, 'image', instance.imageId)

    def get_ingredients(self, instance):
        return ','.join(instance.ingredients.values_list('name', flat=True))


class ProductDetailSerializer(ProductListSerializer):
    class Meta:
        model = Product
        fields = ['id', 'imgUrl', 'name', 'price', 'gender', 'category', 'ingredients', 'monthlySales']


class RecommendProductListSerializer(serializers.ModelSerializer):
    imgUrl = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = ['id', 'imgUrl', 'name', 'price']

    def get_imgUrl(self, instance):
        return '{}/{}/{}'.format(IMAGE_URL, 'thumbnail', instance.imageId)

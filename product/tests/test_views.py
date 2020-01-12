from random import randint, randrange, choice

from django.test import TestCase

from product.models import Product, Ingredient


class ProductListAPIViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        number_of_ingredients = 50
        number_of_products = 53

        effect_list = ['O', 'X', '']
        for ingredients_id in range(number_of_ingredients):
            Ingredient.objects.create(
                name='ingredient {}'.format(ingredients_id),
                oily=choice(effect_list),
                dry=choice(effect_list),
                sensitive=choice(effect_list)
            )

        gender_list = ['male', 'female', 'all']
        category_list = ['skincare', 'maskpack', 'suncare', 'basemakeup']
        for product_id in range(number_of_products):

            product = Product.objects.create(
                imageId='image id {}'.format(product_id),
                name='product {}'.format(product_id),
                price=randrange(0, 200000, 1000),
                gender=choice(gender_list),
                category=choice(category_list),
                monthlySales=randint(0, 9999),
            )
            for ingredients_id in range(randint(1, 20)):
                product.ingredients.add(randint(1, number_of_ingredients))

    def test_view_url_without_query_params_skin_type(self):
        response = self.client.get('/products/')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'error': '피부 타입은 필수 입력값입니다.'})

    def test_view_url_with_query_params_skin_type_and_this_same_include_ingredient_and_exclude_ingredient(self):
        response = self.client.get('/products/?skin_type=oily&include_ingredient=ingredient 1&exclude_ingredient=ingredient 1')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.data, {'error': '포함과 불포함 성분은 같을 수 없습니다.'})

    def test_view_url_with_query_params_skin_type(self):
        response = self.client.get('/products/?skin_type=oily')
        self.assertEqual(response.status_code, 200)

    def test_view_url_with_query_params_skin_type_and_category(self):
        response = self.client.get('/products/?skin_type=oily&category=skincare')
        self.assertEqual(response.status_code, 200)

    def test_view_url_with_query_params_skin_type_and_page(self):
        response = self.client.get('/products/?skin_type=oily&page=1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_with_query_params_skin_type_and_over_page(self):
        response = self.client.get('/products/?skin_type=oily&page=3')
        self.assertEqual(response.status_code, 404)

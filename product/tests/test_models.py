from random import choice, randrange, randint

from django.test import TestCase

from product.models import Product, Ingredient


class IngredientModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        sample_ingredient = {
            "name": "foundation",
            "oily": "",
            "dry": "X",
            "sensitive": "O"
        }
        Ingredient.objects.create(**sample_ingredient)

    def test_name_label(self):
        ingredient = Ingredient.objects.get(id=1)
        field_label = ingredient._meta.get_field('name').verbose_name
        self.assertEqual(field_label, '이름')

    def test_oily_label(self):
        ingredient = Ingredient.objects.get(id=1)
        field_label = ingredient._meta.get_field('oily').verbose_name
        self.assertEqual(field_label, '지성영향')

    def test_dry_label(self):
        ingredient = Ingredient.objects.get(id=1)
        field_label = ingredient._meta.get_field('dry').verbose_name
        self.assertEqual(field_label, '건성영향')

    def test_sensitive_label(self):
        ingredient = Ingredient.objects.get(id=1)
        field_label = ingredient._meta.get_field('sensitive').verbose_name
        self.assertEqual(field_label, '민감성영향')

    def test_name_max_length(self):
        ingredient = Ingredient.objects.get(id=1)
        max_length = ingredient._meta.get_field('name').max_length
        self.assertEqual(max_length, 64)

    def test_oily_max_length(self):
        ingredient = Ingredient.objects.get(id=1)
        max_length = ingredient._meta.get_field('oily').max_length
        self.assertEqual(max_length, 1)

    def test_dry_max_length(self):
        ingredient = Ingredient.objects.get(id=1)
        max_length = ingredient._meta.get_field('dry').max_length
        self.assertEqual(max_length, 1)

    def test_sensitive_max_length(self):
        ingredient = Ingredient.objects.get(id=1)
        max_length = ingredient._meta.get_field('sensitive').max_length
        self.assertEqual(max_length, 1)

    def test_oily_blank(self):
        ingredient = Ingredient.objects.get(id=1)
        blank = ingredient._meta.get_field('oily').blank
        self.assertTrue(blank)

    def test_dry_blank(self):
        ingredient = Ingredient.objects.get(id=1)
        blank = ingredient._meta.get_field('dry').blank
        self.assertTrue(blank)

    def test_sensitive_blank(self):
        ingredient = Ingredient.objects.get(id=1)
        blank = ingredient._meta.get_field('sensitive').blank
        self.assertTrue(True)


class ProductModelTest(TestCase):
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

    def test_imageId_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('imageId').verbose_name
        self.assertEqual(field_label, '상품 이미지 ID')

    def test_name_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('name').verbose_name
        self.assertEqual(field_label, '상품명')

    def test_price_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('price').verbose_name
        self.assertEqual(field_label, '가격')

    def test_gender_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('gender').verbose_name
        self.assertEqual(field_label, '성별')

    def test_category_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('category').verbose_name
        self.assertEqual(field_label, '카테고리')

    def test_ingredients_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('ingredients').verbose_name
        self.assertEqual(field_label, '구성성분')

    def test_monthlySales_label(self):
        product = Product.objects.get(id=1)
        field_label = product._meta.get_field('monthlySales').verbose_name
        self.assertEqual(field_label, '이번 달 판매 수량')

    def test_imageId_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('imageId').max_length
        self.assertEqual(max_length, 128)

    def test_name_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('name').max_length
        self.assertEqual(max_length, 64)

    def test_gender_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('gender').max_length
        self.assertEqual(max_length, 8)

    def test_category_max_length(self):
        product = Product.objects.get(id=1)
        max_length = product._meta.get_field('category').max_length
        self.assertEqual(max_length, 16)

    def test_ingredients_blank(self):
        product = Product.objects.get(id=1)
        blank = product._meta.get_field('category').blank
        self.assertFalse(blank)

    def test_gender_choices(self):
        product = Product.objects.get(id=1)
        choices = product._meta.get_field('gender').choices
        self.assertEqual(choices, (
            ('male', '남'),
            ('female', '여'),
            ('all', '구분없음'),
        ))

    def test_category_choices(self):
        product = Product.objects.get(id=1)
        choices = product._meta.get_field('category').choices
        self.assertEqual(choices, (
            ('skincare', '스킨케어'),
            ('maskpack', '마스크팩'),
            ('suncare', '선케어'),
            ('basemakeup', '베이스메이크업'),
        ))

    def test_get_score(self):
        product = Product.objects.get(id=1)
        score = product.get_score('oily')
        self.assertEqual(type(score), int)

    def test_manager_get_sorted_query_set(self):
        product_list = Product.objects.get_sorted_query_set('oily', {'category': 'skincare'}, {'ingredients__name__in': 'ingredient 1'})
        self.assertTrue(product_list)

    def test_manager_get_recommend_product_list(self):
        product = Product.objects.get(id=1)
        recommend_product_list = Product.objects.get_recommend_product_list(product.id, 'oily')
        self.assertTrue(recommend_product_list)
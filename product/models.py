from django.db import models


GENDER_CHOICE = (
    ('male', '남'),
    ('female', '여'),
    ('all', '구분없음'),
)

CATEGORY_CHOICE = (
    ('skincare', '스킨케어'),
    ('maskpack', '마스크팩'),
    ('suncare', '선케어'),
    ('basemakeup', '베이스메이크업'),
)


class Ingredient(models.Model):
    name = models.CharField(verbose_name='이름', max_length=128)
    oily = models.CharField(verbose_name='지성영향', max_length=1, blank=True)
    dry = models.CharField(verbose_name='건성영향', max_length=1, blank=True)
    sensitive = models.CharField(verbose_name='민감성영향', max_length=1, blank=True)


class ProductManager(models.Manager):
    def get_sorted_query_set(self, skin_type, product_filter, product_exclude):
        product_list = super(ProductManager, self).filter(**product_filter).exclude(**product_exclude).order_by('price')
        return sorted(product_list, key=lambda p: -p.get_score(skin_type))

    def get_recommend_product_list(self, exclude_pk, skin_type):
        product_list = super(ProductManager, self).exclude(pk=exclude_pk).order_by('price')
        return sorted(product_list, key=lambda p: -p.get_score(skin_type))[:3]


class Product(models.Model):
    imageId = models.CharField(verbose_name='상품 이미지 ID', max_length=128)
    name = models.CharField(verbose_name='상품명', max_length=128)
    price = models.PositiveIntegerField(verbose_name='가격')
    gender = models.CharField(verbose_name='성별', max_length=8, choices=GENDER_CHOICE)
    category = models.CharField(verbose_name='카테고리', max_length=16, choices=CATEGORY_CHOICE)
    ingredients = models.ManyToManyField(Ingredient, verbose_name='구성성분', related_name='products', blank=True)
    monthlySales = models.PositiveIntegerField(verbose_name='이번 달 판매 수량')

    objects = ProductManager()

    def get_score(self, skin_type):
        score = 0
        for ingredient in self.ingredients.all():
            if getattr(ingredient, skin_type) == 'O':
                score += 1
            elif getattr(ingredient, skin_type) == 'X':
                score -= 1
        return score

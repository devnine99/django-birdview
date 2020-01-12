from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from product.models import Product
from product.pagination import ProductListPagination
from product.serializers import ProductListSerializer, ProductDetailSerializer, RecommendProductListSerializer


class ProductListAPIView(ProductListPagination, APIView):
    def get(self, request):
        # get params
        skin_type = request.query_params.get('skin_type')
        category = request.query_params.get('category')
        include_ingredient_param = request.query_params.get('include_ingredient')
        exclude_ingredient_param = request.query_params.get('exclude_ingredient')

        if not skin_type:
            return Response({'error': '피부 타입은 필수 입력값입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        # 포함성분과 불포함성분이 같을 경우 400
        if include_ingredient_param and exclude_ingredient_param:
            include_ingredient_list = include_ingredient_param.split(',')
            exclude_ingredient_list = exclude_ingredient_param.split(',')
            if set(include_ingredient_list).intersection(exclude_ingredient_list):
                return Response({'error': '포함과 불포함 성분은 같을 수 없습니다.'}, status=status.HTTP_400_BAD_REQUEST)

        product_filter = dict()
        product_exclude = dict()

        if category:
            product_filter['category'] = category

        if include_ingredient_param:
            include_ingredient_list = include_ingredient_param.split(',')
            product_filter['ingredients__name__in'] = include_ingredient_list

        if exclude_ingredient_param:
            exclude_ingredient_list = exclude_ingredient_param.split(',')
            product_exclude['ingredients__name__in'] = exclude_ingredient_list

        product_list = Product.objects.get_sorted_query_set(skin_type, product_filter, product_exclude)
        product_list_serializer = ProductListSerializer(self.paginate_queryset(product_list, request), many=True)

        return self.get_paginated_response(product_list_serializer.data)


class ProductDetailAPIView(APIView):
    def get(self, request, pk):
        skin_type = request.query_params.get('skin_type')
        if not skin_type:
            return Response({'error': '피부 타입은 필수 입력값입니다.'}, status=status.HTTP_400_BAD_REQUEST)

        product = Product.objects.get(pk=pk)
        recommend_product_list = Product.objects.get_recommend_product_list(product.pk, skin_type)

        product_serializer = ProductDetailSerializer(product)
        recommend_product_list_serializer = RecommendProductListSerializer(recommend_product_list, many=True)

        return Response([product_serializer.data] + [*recommend_product_list_serializer.data])

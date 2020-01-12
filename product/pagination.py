from rest_framework import pagination
from rest_framework.response import Response


class ProductListPagination(pagination.PageNumberPagination):
    page_size = 50

    def get_paginated_response(self, data):
        return Response(data)

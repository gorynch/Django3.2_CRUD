from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.viewsets import ModelViewSet
from logistic.models import Product, Stock
from logistic.serializers import ProductSerializer, StockSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # при необходимости добавьте параметры фильтрации
    filter_backends = [SearchFilter]
    search_fields = ['title', 'description']


class StockResultsSetPagination(PageNumberPagination):
    page_size = 37
    page_size_query_param = 'page_size'

class StockViewSet(ModelViewSet):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer
    pagination_class = StockResultsSetPagination
    # при необходимости добавьте параметры фильтрации
    # filter_backends = [SearchFilter]
    filter_backends = [SearchFilter, DjangoFilterBackend]
    filterset_fields = ['products']
    search_fields = ['products__title',]
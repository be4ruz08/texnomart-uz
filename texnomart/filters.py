from django_filters import rest_framework as filters
from .models import Product, Category


class ProductFilter(filters.FilterSet):
    min_price = filters.NumberFilter(field_name="price", lookup_expr='gte')
    max_price = filters.NumberFilter(field_name="price", lookup_expr='lte')
    category = filters.CharFilter(field_name="category__name", lookup_expr='exact')
    min_discount = filters.NumberFilter(field_name="discount", lookup_expr='gte')
    max_discount = filters.NumberFilter(field_name="discount", lookup_expr='lte')
    min_rating = filters.NumberFilter(field_name="rating", lookup_expr='gte')
    max_rating = filters.NumberFilter(field_name="rating", lookup_expr='lte')
    min_quantity = filters.NumberFilter(field_name="quantity", lookup_expr='gte')
    max_quantity = filters.NumberFilter(field_name="quantity", lookup_expr='lte')
    liked_by_user = filters.NumberFilter(field_name='likes__id', lookup_expr='exact')

    class Meta:
        model = Product
        fields = [
            'min_price', 'max_price',
            'category', 'min_discount',
            'max_discount', 'min_rating',
            'max_rating', 'min_quantity',
            'max_quantity', 'liked_by_user'
        ]


class CategoryFilter(filters.FilterSet):
    title = filters.CharFilter(field_name="title", lookup_expr='icontains')
    slug = filters.CharFilter(field_name="slug", lookup_expr='exact')

    class Meta:
        model = Category
        fields = ['title', 'slug']

from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
import json
import os
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from texnomart.models import Category, Product
from texnomart.permissions import IsAdminOrStaff
from texnomart.serializers import ProductModelSerializer, CategoryModelSerializer
from rest_framework.pagination import PageNumberPagination
from django.core.cache import caches
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import filters
from django_filters import rest_framework as django_filters
from texnomart.filters import CategoryFilter, ProductFilter


class CategoryListView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]
    pagination_class = PageNumberPagination
    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = CategoryFilter
    search_fields = ['title']

    @method_decorator(cache_page(60 * 3, cache='custom_cache'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class CategoryProductListView(ListAPIView):
    serializer_class = ProductModelSerializer
    pagination_class = PageNumberPagination
    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']

    @method_decorator(cache_page(60 * 3, cache='custom_cache'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)

    def get_queryset(self):
        category_slug = self.kwargs['category_slug']
        category = get_object_or_404(Category, slug=category_slug)
        return Product.objects.filter(group__category=category).select_related('group', 'group__category').prefetch_related('images', 'attributes')


class CategoryCreateView(CreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryModelSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]


class CategoryDeleteView(DestroyAPIView):
    serializer_class = CategoryModelSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def get_object(self):
        category_slug = self.kwargs['category_slug']
        return get_object_or_404(Category, slug=category_slug)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        custom_cache = caches['custom_cache']
        cache_key = f"category_{instance.slug}"
        custom_cache.delete(cache_key)
        data = CategoryModelSerializer(instance).data
        self.save_to_json_file(data, 'pre_delete_category.json')
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def save_to_json_file(self, data, filename):
        file_path = os.path.join(os.getcwd(), filename)
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file)


class CategoryUpdateView(UpdateAPIView):
    serializer_class = CategoryModelSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]

    def cache_update(self, serializer):
        instance = serializer.save()
        custom_cache = caches['custom_cache']
        cache_key = f"category_{instance.slug}"
        custom_cache.delete(cache_key)

    def get_object(self):
        category_slug = self.kwargs['category_slug']
        return get_object_or_404(Category, slug=category_slug)
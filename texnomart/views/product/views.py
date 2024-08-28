from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import ListAPIView, DestroyAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
import json
import os
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import status
from texnomart.models import Product
from texnomart.permissions import IsAdminOrStaff
from texnomart.serializers import ProductModelSerializer
from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework import filters
from django_filters import rest_framework as django_filters
from texnomart.filters import ProductFilter


class ProductListView(ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    permission_classes = [AllowAny]
    authentication_classes = [TokenAuthentication]
    pagination_class = PageNumberPagination
    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['name', 'description']

    @method_decorator(cache_page(60 * 3, cache='default'))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductDetailView(RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    lookup_field = 'id'
    authentication_classes = [JWTAuthentication]

    @method_decorator(cache_page(60 * 3))
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class ProductUpdateView(UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'id'

    def cache_update(self, serializer):
        instance = serializer.save()
        cache_key = f"product_{instance.id}"
        cache.delete(cache_key)


class ProductDeleteView(DestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductModelSerializer
    permission_classes = [IsAuthenticated, IsAdminOrStaff]
    lookup_field = 'id'

    def get_serializer_context(self):
        return {'request': self.request}

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        cache_key = f"product_{instance.id}"
        cache.delete(cache_key)
        serializer = self.get_serializer(instance)
        data = serializer.data
        self.save_to_json_file(data, 'pre_delete_product.json')
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def save_to_json_file(self, data, filename):
        file_path = os.path.join(os.getcwd(), filename)
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file)






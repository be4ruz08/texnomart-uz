from rest_framework.generics import ListAPIView
from texnomart.models import Attribute, KeyModel, ValueModel
from texnomart.serializers import AttributeKeySerializer, AttributeValueSerializer
from rest_framework import filters
from django_filters import rest_framework as django_filters
from rest_framework.pagination import PageNumberPagination


class AttributeKeyListAPIView(ListAPIView):
    serializer_class = AttributeKeySerializer
    pagination_class = PageNumberPagination
    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']

    def get_queryset(self):
        return KeyModel.objects.all()


class AttributeValueListAPIView(ListAPIView):
    serializer_class = AttributeValueSerializer
    pagination_class = PageNumberPagination
    filter_backends = [django_filters.DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['name']
    search_fields = ['name']

    def get_queryset(self):
        return ValueModel.objects.all()


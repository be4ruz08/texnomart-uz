from django.urls import path
from texnomart.views.product.views import (ProductListView, ProductDetailView, ProductUpdateView,
                                           ProductDeleteView)
from texnomart.views.category.views import (CategoryListView, CategoryProductListView, CategoryCreateView,
                                            CategoryUpdateView, CategoryDeleteView)

from texnomart.views.attributes.views import AttributeKeyListAPIView, AttributeValueListAPIView

urlpatterns = [
    path('', ProductListView.as_view(), name='product-list'),
    path('categories/', CategoryListView.as_view(), name='category-list'),
    path('category/<slug:category_slug>/', CategoryProductListView.as_view(), name='category-products'),
    path('category/add-category/', CategoryCreateView.as_view(), name='add-category'),
    path('category/<slug:category_slug>/delete/', CategoryDeleteView.as_view(), name='delete-category'),
    path('category/<slug:category_slug>/edit/', CategoryUpdateView.as_view(), name='edit-category'),
    path('product/detail/<int:id>/', ProductDetailView.as_view(), name='product-detail'),
    path('product/<int:id>/edit/', ProductUpdateView.as_view(), name='edit-product'),
    path('product/<int:id>/delete/', ProductDeleteView.as_view(), name='delete-product'),
    path('attribute-key/', AttributeKeyListAPIView.as_view(), name='attribute-key-list'),
    path('attribute-value/', AttributeValueListAPIView.as_view(), name='attribute-value-list'),
]

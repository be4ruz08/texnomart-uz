from django.contrib import admin

from texnomart.models import Category, Product, Image, Comment, Attribute, KeyModel, ValueModel

# Register your models here.

# admin.site.register(Category)


@admin.register(Category)
class CategoryModelAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('message', 'rating', 'created_at')
    search_fields = ('message',)
    list_filter = ('rating', 'created_at')


admin.site.register(Image)


class AttributeAdmin(admin.ModelAdmin):
    list_display = ('product', 'key', 'value')
    search_fields = ('product__name', 'key', 'value')
    list_filter = ('key',)


admin.site.register(Attribute, AttributeAdmin)

admin.site.register(KeyModel)
admin.site.register(ValueModel)



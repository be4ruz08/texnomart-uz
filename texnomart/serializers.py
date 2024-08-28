from django.db.models import Avg
from rest_framework import serializers
from .models import Product, Category, Attribute, ValueModel, KeyModel


class CategoryModelSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(max_length=None)

    class Meta:
        model = Category
        fields = ['id', 'title', 'slug', 'image']


class ProductModelSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.title')
    is_liked = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    all_images = serializers.SerializerMethodField()
    comment_info = serializers.SerializerMethodField()
    attributes = serializers.SerializerMethodField()

    def get_attributes(self, obj):
        attributes = obj.attributes.all()
        return [{'key': attr.key, 'value': attr.value} for attr in attributes]

    def get_comment_info(self, obj):
        comments = obj.comments.all()
        avg_rating = comments.aggregate(Avg('rating'))['rating__avg'] or 0
        comment_count = comments.count()
        return {'average_rating': avg_rating, 'total_comments': comment_count}

    # def get_all_images(self, instance):
    #     request = self.context.get('request', None)
    #     images = instance.images.all().order_by('-is_primary', '-id')
    #     return [request.build_absolute_uri(image.image.url) for image in images]

    def get_all_images(self, obj):
        images = obj.images.all()
        return [image.image.url for image in images]

    def get_avg_rating(self, obj):
        comments = obj.comments.all()
        avg_rating = comments.aggregate(Avg('rating'))['rating__avg'] or 0
        return avg_rating

    def get_image(self, obj):
        image = obj.images.filter(is_primary=True).first()
        if image:
            request = self.context.get('request')
            return request.build_absolute_uri(image.image.url)

    def get_is_liked(self, obj):
        request = self.context.get('request')
        return obj.likes.filter(id=request.user.id).exists() if request else False

    def get_category_name(self, obj):
        return obj.category.name if obj.category else None

    class Meta:
        model = Product
        fields = ['name', 'description', 'category', 'price', 'discount', 'rating', 'quantity', 'likes', 'comment_info',
                  'attributes', 'category_name', 'is_liked', 'all_images', 'image', 'avg_rating']


class AttributeKeySerializer(serializers.ModelSerializer):
    class Meta:
        model = KeyModel
        fields = ['id', 'name']


class AttributeValueSerializer(serializers.ModelSerializer):
    class Meta:
        model = ValueModel
        fields = ['id', 'name']


class AttributeSerializer(serializers.ModelSerializer):
    key = AttributeKeySerializer()
    value = AttributeValueSerializer()

    class Meta:
        model = Attribute
        fields = ['product', 'key', 'value']


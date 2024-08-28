from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Comment, Product, Image, Category
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.core.mail import send_mail


@receiver(post_save, sender=Comment)
def update_product_rating(sender, instance, **kwargs):
    product = instance.product
    product.calculate_rating()


@receiver(post_delete, sender=Comment)
def update_product_rating_on_delete(sender, instance, **kwargs):
    product = instance.product
    product.calculate_rating()


@receiver(post_delete, sender=Product)
def delete_related_images(sender, instance, **kwargs):
    instance.images.all().delete()


@receiver(post_save, sender=User)
def create_or_update_user_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(user=instance)
    else:
        instance.auth_token.save()


@receiver(post_save, sender=Product)
def create_product(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject='New Product Created',
            message=f'Product "{instance.name}" was created in "{instance.category.title}".',
            from_email='bexruzbxdrv@gmail.com',
            # recipient_list=['goldhamster035@gmail.com'],
            recipient_list=['jasurmavlonov24@gmail.com'],
            fail_silently=False,
        )


@receiver(post_save, sender=Category)
def create_category(sender, instance, created, **kwargs):
    if created:
        send_mail(
            subject='New Category Created',
            message=f'Category "{instance.title}" was created.',
            from_email='bexruzbxdrv@gmail.com',
            recipient_list=['jasurmavlonov24@gmail.com'],
            fail_silently=False,
        )

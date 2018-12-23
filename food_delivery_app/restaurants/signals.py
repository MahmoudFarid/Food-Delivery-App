from django.dispatch import receiver
from django.db.models.signals import post_save

from .models import Restaurant


@receiver(post_save, sender=Restaurant, dispatch_uid='add_users_to_restaurant')
def add_users_to_restaurant(sender, instance, created, **kwargs):
    if instance.users.count() == 0 and instance.owner not in instance.users.all():
        instance.users.add(instance.owner)

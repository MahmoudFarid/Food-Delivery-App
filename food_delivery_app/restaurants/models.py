from django.db import models
from django.db.models.functions import Coalesce
from django.db.models import Sum
from django.utils.translation import ugettext_lazy as _
from django.core.validators import RegexValidator
from django.conf import settings

from django_extensions.db.models import TimeStampedModel

from food_delivery_app.core.utils import media_file_name


def item_images(instance, filename):
    return media_file_name('items', 'restaurant_id')(instance, filename)


def restaurant_images(instance, filename):
    return media_file_name('restaurant', 'owner_id')(instance, filename)


phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Phone number must be entered in the format: '+9999999'. Up to 15 digits allowed.")


class Restaurant(TimeStampedModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='my_restaurants')
    users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='restaurants', blank=True)
    name = models.CharField(_('Name'), max_length=128)
    phone = models.CharField(_('Phone'), validators=[phone_regex], max_length=128)
    address = models.CharField(_('Address'), max_length=128)
    logo = models.ImageField(_('Logo'), upload_to=restaurant_images, blank=True, null=True)

    def __str__(self):
        return self.name


class ItemCategory(TimeStampedModel):
    name = models.CharField(_('Name'), max_length=128)

    class Meta:
        verbose_name = 'Item category'
        verbose_name_plural = 'Item categories'

    def __str__(self):
        return self.name


class ItemSize(TimeStampedModel):
    name = models.CharField(_('Name'), max_length=128)

    class Meta:
        verbose_name = 'Item size'
        verbose_name_plural = 'Item sizes'

    def __str__(self):
        return self.name


class Item(TimeStampedModel):
    restaurant = models.ForeignKey("Restaurant", related_name='items', on_delete=models.CASCADE)
    category = models.ForeignKey("ItemCategory", related_name='items', on_delete=models.PROTECT)
    size = models.ManyToManyField("ItemSize", related_name='items', blank=True)
    name = models.CharField(max_length=128)
    short_description = models.CharField(max_length=128)
    image = models.ImageField(upload_to=item_images)
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Order(TimeStampedModel):
    PICKED = 1
    COOKING = 2
    READY = 3
    ONTHEWAY = 4
    DELIVERED = 5
    CANCELLED = 6
    STATUS_CHOICES = (
        (PICKED, _("Picked")),
        (COOKING, _("Cooking")),
        (READY, _("Ready")),
        (ONTHEWAY, _("On the way")),
        (DELIVERED, _("Delivered")),
        (CANCELLED, _("Candelled")),
    )

    customer = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='orders', on_delete=models.CASCADE)
    restaurant = models.ForeignKey("Restaurant", related_name='orders', on_delete=models.CASCADE)
    items = models.ManyToManyField("Item", related_name="orders", through='ItemOrderDetails')
    address = models.CharField(max_length=500)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PICKED)
    cooked_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

    @property
    def total_price(self):
        return self.items.aggregate(price=Coalesce(Sum('price'), 0)).get('price')


class ItemOrderDetails(models.Model):
    item = models.ForeignKey("Item", on_delete=models.CASCADE)
    order = models.ForeignKey("Order", on_delete=models.CASCADE)
    count = models.IntegerField(default=1)
    size = models.ForeignKey("ItemSize", on_delete=models.PROTECT, null=True, blank=True)

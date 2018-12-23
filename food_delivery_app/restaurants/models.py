from django.db import models
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


class Category(TimeStampedModel):
    restaurant = models.ForeignKey("Restaurant", related_name='categories', on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=128)

    class Meta:
        verbose_name = 'Item category'
        verbose_name_plural = 'Item categories'
        unique_together = ('name', 'restaurant')

    def __str__(self):
        return self.name


class ItemSize(TimeStampedModel):
    restaurant = models.ForeignKey("Restaurant", related_name='item_sizes', on_delete=models.CASCADE)
    name = models.CharField(_('Name'), max_length=128)

    class Meta:
        verbose_name = 'Item size'
        verbose_name_plural = 'Item sizes'
        unique_together = ('name', 'restaurant')

    def __str__(self):
        return self.name


class Item(TimeStampedModel):
    restaurant = models.ForeignKey("Restaurant", related_name='items', on_delete=models.CASCADE)
    category = models.ForeignKey("Category", related_name='items', on_delete=models.PROTECT)
    sizes = models.ManyToManyField("ItemSize", related_name='items', through='ItemSizeDetails')
    name = models.CharField(max_length=128)
    short_description = models.CharField(max_length=128)
    image = models.ImageField(upload_to=item_images, null=True, blank=True)

    def __str__(self):
        return self.name


class ItemSizeDetails(models.Model):
    item = models.ForeignKey("Item", on_delete=models.CASCADE, related_name='size_details')
    size = models.ForeignKey("ItemSize", on_delete=models.CASCADE, related_name='size_details')
    price = models.IntegerField(default=1)

    class Meta:
        unique_together = ('item', 'size')

    def __str__(self):
        return str(self.id)


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
    items_sizes = models.ManyToManyField("ItemSizeDetails", related_name="orders", through='ItemOrderDetails')
    address = models.CharField(max_length=500)
    status = models.IntegerField(choices=STATUS_CHOICES, default=PICKED)
    total_price = models.IntegerField(default=0)

    cooked_at = models.DateTimeField(blank=True, null=True)
    ready_at = models.DateTimeField(blank=True, null=True)
    on_the_way_at = models.DateTimeField(blank=True, null=True)
    delivered_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return str(self.id)

    def get_total_price(self):
        '''
            Don't depend on this method, it'll get the updated price based on related objects
            use total_price field instead of this method
            we use this method to save/update total_price field when the order is created/updated
        '''
        total = 0
        for order_detail in self.orders_details.all():
            total += order_detail.get_total_items_price()
        return total


class ItemOrderDetails(models.Model):
    item_size = models.ForeignKey("ItemSizeDetails", on_delete=models.PROTECT, related_name='orders_details')
    order = models.ForeignKey("Order", on_delete=models.CASCADE, related_name='orders_details')
    count = models.IntegerField(default=1)

    def __str__(self):
        return str(self.id)

    def get_total_items_price(self):
        return self.item_size.price * self.count

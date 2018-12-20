from django.contrib import admin

from .models import Restaurant, ItemCategory, ItemSize, Item


admin.site.register(Restaurant)
admin.site.register(ItemCategory)
admin.site.register(ItemSize)
admin.site.register(Item)

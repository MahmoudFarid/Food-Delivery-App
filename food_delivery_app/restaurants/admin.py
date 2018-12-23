from django.contrib import admin

from .models import Restaurant, Category, ItemSize, Item


admin.site.register(Restaurant)
admin.site.register(Category)
admin.site.register(ItemSize)
admin.site.register(Item)

from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions

from .serializers import RestaurantSerializer, CategorySerializer, ItemSizeSerializer, ItemSerializer
from .models import Restaurant, Item, ItemSize, Category

User = get_user_model()


class RestaurantViewSet(viewsets.ModelViewSet):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        restaurant = serializer.save()
        if restaurant.users.count() == 0 and restaurant.owner not in restaurant.users.all():
            restaurant.users.add(restaurant.owner)


class ItemSizeViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """
    queryset = ItemSize.objects.all()
    serializer_class = ItemSizeSerializer

    def get_queryset(self):
        restaurant_id = int(self.kwargs.get('restaurant_id'))
        return super().get_queryset().filter(restaurant_id=restaurant_id)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    A simple ViewSet for viewing accounts.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_queryset(self):
        restaurant_id = int(self.kwargs.get('restaurant_id'))
        return super().get_queryset().filter(restaurant_id=restaurant_id)


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    queryset = Item.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        restaurant_id = int(self.kwargs.get('restaurant_id'))
        return super().get_queryset().filter(restaurant_id=restaurant_id)

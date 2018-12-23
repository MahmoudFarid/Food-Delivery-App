from django.contrib.auth import get_user_model
from rest_framework import serializers

from food_delivery_app.users.serializers import UserSerializer

from .models import Restaurant, Item, ItemSize, Category

User = get_user_model()


class RestaurantDefault:
    def set_context(self, serializer_field):
        restaurant_id = serializer_field.context['view'].kwargs['restaurant_id']
        self.restaurant = Restaurant.objects.get(pk=restaurant_id)

    def __call__(self):
        return self.restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
    users = UserSerializer(many=True, required=False)

    class Meta:
        model = Restaurant
        fields = ('id', 'owner', 'users', 'name', 'phone', 'address', 'logo')


class ItemSizeSerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(), default=RestaurantDefault())

    class Meta:
        model = ItemSize
        fields = ('id', 'name', 'restaurant')


class CategorySerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(), default=RestaurantDefault())

    class Meta:
        model = Category
        fields = ('id', 'name', 'restaurant')


class ItemSerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(), default=RestaurantDefault())

    class Meta:
        model = Item
        fields = ('id', 'restaurant', 'category', 'size', 'name', 'short_description', 'image', 'price')

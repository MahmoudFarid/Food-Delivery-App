from django.contrib.auth import get_user_model
from rest_framework import serializers

from food_delivery_app.users.serializers import UserSerializer

from .models import Restaurant, Item, ItemSize, Category, Order, ItemOrderDetails, ItemSizeDetails

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


class ItemSizeDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemSizeDetails
        fields = ('id', 'size', 'price')


class ItemSerializer(serializers.ModelSerializer):
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(), default=RestaurantDefault())
    item_sizes = ItemSizeDetailsSerializer(many=True, write_only=True)
    size_details = ItemSizeDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = ('id', 'restaurant', 'category', 'name', 'short_description', 'image', 'size_details', 'item_sizes')


class ItemOrderDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = ItemOrderDetails
        fields = ('id', 'item_size', 'count')


class OrderSerializer(serializers.ModelSerializer):
    customer = UserSerializer(default=serializers.CurrentUserDefault())
    restaurant = serializers.PrimaryKeyRelatedField(queryset=Restaurant.objects.all(), default=RestaurantDefault())
    items_sizes = ItemOrderDetailsSerializer(many=True, write_only=True)
    orders_details = ItemOrderDetailsSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'restaurant', 'customer', 'orders_details', 'items_sizes', 'address', 'total_price', 'status',
                  'cooked_at', 'ready_at', 'on_the_way_at', 'delivered_at')
        read_only_fields = ('cooked_at', 'ready_at', 'on_the_way_at', 'delivered_at', 'status', 'orders_details',
                            'customer', 'total_price')

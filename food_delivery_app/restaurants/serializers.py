from django.contrib.auth import get_user_model
from rest_framework import serializers

from food_delivery_app.users.serializers import UserSerializer

from .models import Restaurant

User = get_user_model()


class RestaurantSerializer(serializers.ModelSerializer):
    owner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())
    users = UserSerializer(many=True, required=False)

    class Meta:
        model = Restaurant
        fields = ('id', 'owner', 'users', 'name', 'phone', 'address', 'logo')

from django.contrib.auth import get_user_model
from rest_framework import viewsets, permissions

from .serializers import RestaurantSerializer
from .models import Restaurant

User = get_user_model()


class RestaurantViewSet(viewsets.ModelViewSet):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        restaurant = serializer.save()
        if restaurant.users.count() == 0 and restaurant.owner not in restaurant.users.all():
            restaurant.users.add(restaurant.owner)

from django.contrib.auth import get_user_model
from django.db.models import ProtectedError
from rest_framework import viewsets, permissions
from rest_framework.exceptions import ValidationError

from django_filters.rest_framework import DjangoFilterBackend

from .serializers import RestaurantSerializer, CategorySerializer, ItemSizeSerializer, ItemSerializer, OrderSerializer
from .models import Restaurant, Item, ItemSize, Category, Order, ItemOrderDetails, ItemSizeDetails
from .filters import OrderFilter

User = get_user_model()


class RestaurantViewSet(viewsets.ModelViewSet):
    serializer_class = RestaurantSerializer
    queryset = Restaurant.objects.all()
    permission_classes = [permissions.IsAuthenticated]


class ItemSizeViewSet(viewsets.ModelViewSet):
    queryset = ItemSize.objects.all()
    serializer_class = ItemSizeSerializer

    def get_queryset(self):
        restaurant_id = int(self.kwargs.get('restaurant_id'))
        return super().get_queryset().filter(restaurant_id=restaurant_id)


class CategoryViewSet(viewsets.ModelViewSet):
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

    def perform_create(self, serializer):
        item_sizes = serializer.validated_data.pop('item_sizes')
        item = serializer.save()
        for item_size in item_sizes:
            ItemSizeDetails.objects.create(item=item, **item_size)
        return item

    def perform_update(self, serializer):
        item_sizes = serializer.validated_data.pop('item_sizes')
        item = serializer.instance
        for field in serializer.validated_data:
            if Item._meta.get_field(field):
                setattr(item, field, serializer.validated_data[field])

        item_sizes_ids = []
        for item_size in item_sizes:
            item_sizes = ItemSizeDetails.objects.filter(item=item, size=item_size.get('size'))
            if item_sizes.exists():
                item_sizes.update(price=item_size.get('price'))
                item_sizes_ids.append(item_sizes.first().pk)
            else:
                item_size = ItemSizeDetails.objects.create(item=item, **item_size)
                item_sizes_ids.append(item_size.pk)

        try:
            ItemSizeDetails.objects.exclude(pk__in=item_sizes_ids).delete()
        except ProtectedError as e:
            raise ValidationError({"errors": e})
        item.save()
        return item


class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    queryset = Order.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = OrderFilter

    def get_queryset(self):
        restaurant_id = int(self.kwargs.get('restaurant_id'))
        return super().get_queryset().filter(restaurant_id=restaurant_id)

    def perform_create(self, serializer):
        items_sizes = serializer.validated_data.pop('items_sizes')
        order = serializer.save()
        for item_size in items_sizes:
            ItemOrderDetails.objects.create(order=order, **item_size)

        order.total_price = order.get_total_price()
        order.save()
        return order

    def perform_update(self, serializer):
        items_sizes = serializer.validated_data.pop('items_sizes')
        order = serializer.instance
        for field in serializer.validated_data:
            if Order._meta.get_field(field):
                setattr(order, field, serializer.validated_data[field])
        ItemOrderDetails.objects.filter(order=order).delete()
        for item_size in items_sizes:
            ItemOrderDetails.objects.create(order=order, **item_size)

        order.total_price = order.get_total_price()
        order.save()
        return order

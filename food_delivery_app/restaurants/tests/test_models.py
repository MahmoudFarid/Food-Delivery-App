from django.test import TestCase

from ..models import Restaurant, Category, ItemSize, Item, ItemSizeDetails, Order, ItemOrderDetails
from .factories import (RestaurantFactory, CategoryFactory, ItemSizeFactory, ItemFactory, ItemSizeDetailsFactory,
                        OrderFactory, ItemOrderDetailsFactory)


class TestRestaurantModel(TestCase):

    def test_create_restaurant(self):
        restaurant = RestaurantFactory.create()
        self.assertIsInstance(restaurant, Restaurant)
        self.assertEqual(Restaurant.objects.count(), 1)

    def test_create_category(self):
        category = CategoryFactory.create()
        self.assertIsInstance(category, Category)
        self.assertEqual(Category.objects.count(), 1)

    def test_create_item_size(self):
        item_size = ItemSizeFactory.create()
        self.assertIsInstance(item_size, ItemSize)
        self.assertEqual(ItemSize.objects.count(), 1)

    def test_create_item(self):
        item = ItemFactory.create()
        self.assertIsInstance(item, Item)
        self.assertEqual(Item.objects.count(), 1)

    def test_create_item_size_details(self):
        item_size_details = ItemSizeDetailsFactory.create()
        self.assertIsInstance(item_size_details, ItemSizeDetails)
        self.assertEqual(ItemSizeDetails.objects.count(), 1)

    def test_create_order(self):
        order = OrderFactory.create()
        self.assertIsInstance(order, Order)
        self.assertEqual(Order.objects.count(), 1)

    def test_create_item_order_details(self):
        item_order_details = ItemOrderDetailsFactory.create()
        self.assertIsInstance(item_order_details, ItemOrderDetails)
        self.assertEqual(ItemOrderDetails.objects.count(), 1)

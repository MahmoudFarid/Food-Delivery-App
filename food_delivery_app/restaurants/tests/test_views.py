import json

from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.authtoken.models import Token

from food_delivery_app.users.tests.factories import UserFactory

from ..models import Restaurant, Category, ItemSize, Item, Order
from .factories import (RestaurantFactory, CategoryFactory, ItemSizeFactory, ItemFactory, ItemSizeDetailsFactory,
                        OrderFactory, ItemOrderDetailsFactory, create_item_with_sizes)


class TestRestaurantAPIViews(APITestCase):

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)

    def test_list_restaurants(self):
        RestaurantFactory.create_batch(10)
        url = reverse("api_v1:restaurants-list")

        response = self.client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Restaurant.objects.count(), response.data.get('count'))

    def test_create_restaurant(self):
        url = reverse("api_v1:restaurants-list")
        data = {
            "name": "Test Restaurant",
            "phone": "00201012345678",
            "address": "Cairo"
        }

        self.assertEqual(Restaurant.objects.count(), 0)
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Restaurant.objects.count(), 1)

    def test_update_restaurant(self):
        restaurant = RestaurantFactory()
        self.assertEqual(Restaurant.objects.count(), 1)

        url = reverse("api_v1:restaurants-detail", kwargs={"pk": restaurant.pk})
        data = {
            "name": "Updated Restaurant",
            "phone": "00201012345678",
            "address": "Cairo"
        }

        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(Restaurant.objects.count(), 1)
        restaurant = Restaurant.objects.last()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(restaurant.name, data.get('name'))
        self.assertEqual(restaurant.phone, data.get('phone'))
        self.assertEqual(restaurant.address, data.get('address'))

    def test_delete_restaurant(self):
        restaurant = RestaurantFactory()
        self.assertEqual(Restaurant.objects.count(), 1)

        url = reverse("api_v1:restaurants-detail", kwargs={"pk": restaurant.pk})

        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Restaurant.objects.count(), 0)


class TestCategoryAPIViews(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.restaurant = RestaurantFactory()

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.restaurant = self.restaurant

    def test_list_categories(self):
        CategoryFactory.create_batch(10, restaurant=self.restaurant)
        CategoryFactory.create_batch(5)
        url = reverse("api_v1:categories-list", kwargs={"restaurant_id": self.restaurant.pk})

        response = self.client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Category.objects.count(), 15)
        self.assertEqual(Category.objects.filter(restaurant=self.restaurant).count(), response.data.get('count'))
        self.assertEqual(10, response.data.get('count'))

    def test_create_category(self):
        url = reverse("api_v1:categories-list", kwargs={"restaurant_id": self.restaurant.pk})
        data = {
            "name": "Main Course"
        }
        self.assertEqual(Category.objects.count(), 0)
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(Category.objects.last().restaurant, self.restaurant)

    def test_update_category(self):
        category = CategoryFactory(restaurant=self.restaurant)
        self.assertEqual(Category.objects.count(), 1)

        url = reverse("api_v1:categories-detail", kwargs={"restaurant_id": self.restaurant.pk, "pk": category.pk})
        data = {
            "name": "Main Course",
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(Category.objects.count(), 1)
        category = Category.objects.last()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(category.name, data.get('name'))

    def test_delete_category(self):
        category = CategoryFactory(restaurant=self.restaurant)
        self.assertEqual(Category.objects.count(), 1)

        url = reverse("api_v1:categories-detail", kwargs={"restaurant_id": self.restaurant.pk, "pk": category.pk})

        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Category.objects.count(), 0)


class TestItemSizeAPIViews(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.restaurant = RestaurantFactory()

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.restaurant = self.restaurant

    def test_list_item_sizes(self):
        ItemSizeFactory.create_batch(10, restaurant=self.restaurant)
        ItemSizeFactory.create_batch(5)
        url = reverse("api_v1:item_sizes-list", kwargs={"restaurant_id": self.restaurant.pk})

        response = self.client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(ItemSize.objects.count(), 15)
        self.assertEqual(ItemSize.objects.filter(restaurant=self.restaurant).count(), response.data.get('count'))
        self.assertEqual(10, response.data.get('count'))

    def test_create_item_size(self):
        url = reverse("api_v1:item_sizes-list", kwargs={"restaurant_id": self.restaurant.pk})
        data = {
            "name": "Large"
        }
        self.assertEqual(ItemSize.objects.count(), 0)
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(ItemSize.objects.count(), 1)
        self.assertEqual(ItemSize.objects.last().restaurant, self.restaurant)

    def test_update_item_size(self):
        item_size = ItemSizeFactory(restaurant=self.restaurant)
        self.assertEqual(ItemSize.objects.count(), 1)

        url = reverse("api_v1:item_sizes-detail", kwargs={"restaurant_id": self.restaurant.pk, "pk": item_size.pk})
        data = {
            "name": "Meduim",
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(ItemSize.objects.count(), 1)
        item_size = ItemSize.objects.last()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(item_size.name, data.get('name'))

    def test_delete_item_size(self):
        item_size = ItemSizeFactory(restaurant=self.restaurant)
        self.assertEqual(ItemSize.objects.count(), 1)

        url = reverse("api_v1:item_sizes-detail", kwargs={"restaurant_id": self.restaurant.pk, "pk": item_size.pk})

        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(ItemSize.objects.count(), 0)


class TestItemAPIViews(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.restaurant = RestaurantFactory()
        cls.category = CategoryFactory(restaurant=cls.restaurant)
        cls.item_size1 = ItemSizeFactory(restaurant=cls.restaurant)
        cls.item_size2 = ItemSizeFactory(restaurant=cls.restaurant)

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.restaurant = self.restaurant
        self.category = self.category
        self.item_size1 = self.item_size1
        self.item_size2 = self.item_size2

    def test_list_items(self):
        ItemFactory.create_batch(10, restaurant=self.restaurant)
        ItemFactory.create_batch(5)
        url = reverse("api_v1:items-list", kwargs={"restaurant_id": self.restaurant.pk})

        response = self.client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Item.objects.count(), 15)
        self.assertEqual(Item.objects.filter(restaurant=self.restaurant).count(), response.data.get('count'))
        self.assertEqual(10, response.data.get('count'))

    def test_create_item(self):
        url = reverse("api_v1:items-list", kwargs={"restaurant_id": self.restaurant.pk})
        data = {
            "category": self.category.pk,
            "name": "Chicken Pizza",
            "short_description": "Delecious Pizza!",
            "item_sizes": [
                {"size": self.item_size1.pk, "price": 50},
                {"size": self.item_size2.pk, "price": 100}
            ]
        }
        self.assertEqual(Item.objects.count(), 0)
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.last()
        self.assertEqual(item.restaurant, self.restaurant)
        self.assertEqual(item.category, self.category)
        self.assertEqual(item.sizes.count(), 2)
        self.assertTrue(item.sizes.filter(pk=self.item_size1.pk).exists())
        self.assertTrue(item.sizes.filter(pk=self.item_size2.pk).exists())

    def test_update_item(self):
        item = create_item_with_sizes(self.restaurant, 5)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(item.sizes.count(), 5)

        url = reverse("api_v1:items-detail", kwargs={"restaurant_id": self.restaurant.pk, "pk": item.pk})
        data = {
            "category": self.category.pk,
            "name": "Meat Pizza",
            "short_description": "Delecious Pizza!",
            "item_sizes": [
                {"size": self.item_size1.pk, "price": 50},
                {"size": self.item_size2.pk, "price": 100}
            ]
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.last()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(item.name, data.get('name'))
        self.assertEqual(item.short_description, data.get('short_description'))
        self.assertEqual(item.sizes.count(), 2)
        self.assertTrue(item.sizes.filter(pk=self.item_size1.pk).exists())
        self.assertTrue(item.sizes.filter(pk=self.item_size2.pk).exists())

    def test_update_item_size_price(self):
        item = ItemFactory(restaurant=self.restaurant)
        ItemSizeDetailsFactory(item=item, size=self.item_size1, price=100)
        ItemSizeDetailsFactory(item=item, size=self.item_size2, price=200)

        self.assertEqual(item.size_details.get(size_id=self.item_size1.pk).price, 100)
        self.assertEqual(item.size_details.get(size_id=self.item_size2.pk).price, 200)

        url = reverse("api_v1:items-detail", kwargs={"restaurant_id": self.restaurant.pk, "pk": item.pk})
        data = {
            "category": self.category.pk,
            "name": "Meat Pizza",
            "short_description": "Delecious Pizza!",
            "item_sizes": [
                {"size": self.item_size1.pk, "price": 40},
                {"size": self.item_size2.pk, "price": 80}
            ]
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.last()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(item.size_details.get(size_id=self.item_size1.pk).price, 40)
        self.assertEqual(item.size_details.get(size_id=self.item_size2.pk).price, 80)

    def test_delete_item_size_price(self):
        item = ItemFactory(restaurant=self.restaurant)
        ItemSizeDetailsFactory(item=item, size=self.item_size1, price=100)
        ItemSizeDetailsFactory(item=item, size=self.item_size2, price=200)

        url = reverse("api_v1:items-detail", kwargs={"restaurant_id": self.restaurant.pk, "pk": item.pk})
        data = {
            "category": self.category.pk,
            "name": "Meat Pizza",
            "short_description": "Delecious Pizza!",
            "item_sizes": [
                {"size": self.item_size1.pk, "price": 40},
            ]
        }
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(Item.objects.count(), 1)
        item = Item.objects.last()
        self.assertEqual(response.status_code, 200)
        self.assertFalse(item.size_details.filter(size_id=self.item_size2.pk).exists())

    def test_delete_item(self):
        item = create_item_with_sizes(self.restaurant, 5)
        self.assertEqual(Item.objects.count(), 1)
        self.assertEqual(item.sizes.count(), 5)

        url = reverse("api_v1:items-detail", kwargs={"restaurant_id": self.restaurant.pk, "pk": item.pk})

        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Item.objects.count(), 0)


class TestOrderAPIViews(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.restaurant = RestaurantFactory()

        cls.item1 = ItemFactory(restaurant=cls.restaurant)
        cls.item2 = ItemFactory(restaurant=cls.restaurant)
        cls.item_size1 = ItemSizeFactory(restaurant=cls.restaurant)
        cls.item_size2 = ItemSizeFactory(restaurant=cls.restaurant)
        cls.item_size_details1 = ItemSizeDetailsFactory(item=cls.item1, size=cls.item_size1, price=100)
        cls.item_size_details2 = ItemSizeDetailsFactory(item=cls.item1, size=cls.item_size2, price=200)
        cls.item_size_details3 = ItemSizeDetailsFactory(item=cls.item2, size=cls.item_size1, price=300)
        cls.item_size_details4 = ItemSizeDetailsFactory(item=cls.item2, size=cls.item_size2, price=400)

    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        token, _ = Token.objects.get_or_create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
        self.restaurant = self.restaurant
        self.item1 = self.item1
        self.item2 = self.item2
        self.item_size1 = self.item_size1
        self.item_size2 = self.item_size2
        self.item_size_details1 = self.item_size_details1
        self.item_size_details2 = self.item_size_details2
        self.item_size_details3 = self.item_size_details3
        self.item_size_details4 = self.item_size_details4

    def test_list_orders(self):
        OrderFactory.create_batch(10, restaurant=self.restaurant)
        OrderFactory.create_batch(5)
        url = reverse("api_v1:orders-list", kwargs={"restaurant_id": self.restaurant.pk})

        response = self.client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 15)
        self.assertEqual(Order.objects.filter(restaurant=self.restaurant).count(), response.data.get('count'))
        self.assertEqual(10, response.data.get('count'))

    def test_filter_list_orders_by_customers(self):
        customer1 = UserFactory()
        customer2 = UserFactory()
        OrderFactory.create_batch(10, restaurant=self.restaurant, customer=customer1)
        OrderFactory.create_batch(5, restaurant=self.restaurant, customer=customer2)

        url = (reverse("api_v1:orders-list", kwargs={"restaurant_id": self.restaurant.pk}) +
               "?customer={}".format(customer1.pk))
        response = self.client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(10, response.data.get('count'))

        url = (reverse("api_v1:orders-list", kwargs={"restaurant_id": self.restaurant.pk}) +
               "?customer={}".format(customer2.pk))
        response = self.client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(5, response.data.get('count'))

    def test_filter_list_orders_by_status(self):
        OrderFactory.create_batch(5, restaurant=self.restaurant, status=1)
        OrderFactory.create_batch(6, restaurant=self.restaurant, status=2)
        OrderFactory.create_batch(7, restaurant=self.restaurant, status=3)

        url = reverse("api_v1:orders-list", kwargs={"restaurant_id": self.restaurant.pk}) + "?status={}".format(1)
        response = self.client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(5, response.data.get('count'))

        url = (reverse("api_v1:orders-list", kwargs={"restaurant_id": self.restaurant.pk}) + "?status={}".format(2))
        response = self.client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(6, response.data.get('count'))

        url = (reverse("api_v1:orders-list", kwargs={"restaurant_id": self.restaurant.pk}) + "?status={}".format(3))
        response = self.client.get(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(7, response.data.get('count'))

    def test_create_order(self):
        url = reverse("api_v1:orders-list", kwargs={"restaurant_id": self.restaurant.pk})
        data = {
            "items_sizes": [
                {"item_size": self.item_size_details1.pk, "count": 1},
                {"item_size": self.item_size_details2.pk, "count": 2},
                {"item_size": self.item_size_details3.pk, "count": 3},
                {"item_size": self.item_size_details4.pk, "count": 4},
            ],
            "address": "Cairo"
        }

        self.assertEqual(Order.objects.count(), 0)
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.last()
        self.assertEqual(order.restaurant, self.restaurant)
        self.assertEqual(order.total_price, 3000)  # 1 * 100 + 2 * 200 + 3 * 300 + 4 * 400
        self.assertEqual(order.status, 1)
        self.assertEqual(order.address, data.get('address'))
        self.assertEqual(order.items_sizes.count(), 4)
        self.assertTrue(order.items_sizes.filter(pk=self.item_size_details1.pk).exists())
        self.assertTrue(order.items_sizes.filter(pk=self.item_size_details2.pk).exists())
        self.assertTrue(order.items_sizes.filter(pk=self.item_size_details3.pk).exists())
        self.assertTrue(order.items_sizes.filter(pk=self.item_size_details4.pk).exists())

    def test_create_order_then_update_item_price(self):
        url = reverse("api_v1:orders-list", kwargs={"restaurant_id": self.restaurant.pk})
        data = {
            "items_sizes": [
                {"item_size": self.item_size_details1.pk, "count": 3},
            ],
            "address": "Cairo"
        }

        self.assertEqual(Order.objects.count(), 0)
        self.assertEqual(self.item_size_details1.price, 100)
        response = self.client.post(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.last()
        self.assertEqual(order.total_price, 300)  # 3 * 100
        self.assertEqual(order.total_price, order.get_total_price())

        self.item_size_details1.price = 600
        self.item_size_details1.save()
        order.refresh_from_db()
        self.assertEqual(order.total_price, 300)
        self.assertNotEqual(order.total_price, order.get_total_price())
        self.assertEqual(order.get_total_price(), 1800)  # 3 * 1800

    def test_update_order_item_count(self):
        order = OrderFactory(restaurant=self.restaurant, total_price=0)
        ItemOrderDetailsFactory(order=order, item_size=self.item_size_details1, count=1)
        ItemOrderDetailsFactory(order=order, item_size=self.item_size_details1, count=2)
        ItemOrderDetailsFactory(order=order, item_size=self.item_size_details1, count=3)
        ItemOrderDetailsFactory(order=order, item_size=self.item_size_details1, count=4)

        url = reverse("api_v1:orders-detail", kwargs={"restaurant_id": self.restaurant.pk, "pk": order.pk})

        data = {
            "items_sizes": [
                {"item_size": self.item_size_details1.pk, "count": 4},
                {"item_size": self.item_size_details2.pk, "count": 3},
                {"item_size": self.item_size_details3.pk, "count": 2},
                {"item_size": self.item_size_details4.pk, "count": 1},
            ],
            "address": "New Cairo"
        }

        self.assertEqual(order.total_price, 0)

        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.last()
        self.assertEqual(order.total_price, 2000)  # 4 * 100 + 3 * 200 + 2 * 300 + 1 * 400
        self.assertEqual(order.address, data.get('address'))
        self.assertEqual(order.items_sizes.count(), 4)

    def test_update_order_by_remove_item(self):
        order = OrderFactory(restaurant=self.restaurant)
        ItemOrderDetailsFactory(order=order, item_size=self.item_size_details2, count=2)
        ItemOrderDetailsFactory(order=order, item_size=self.item_size_details3, count=3)
        ItemOrderDetailsFactory(order=order, item_size=self.item_size_details4, count=4)

        url = reverse("api_v1:orders-detail", kwargs={"restaurant_id": self.restaurant.pk, "pk": order.pk})

        data = {
            "items_sizes": [
                {"item_size": self.item_size_details1.pk, "count": 4},
                {"item_size": self.item_size_details2.pk, "count": 3},
            ],
            "address": "New Cairo"
        }

        self.assertEqual(order.items_sizes.count(), 3)

        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        response = self.client.put(url, data=json.dumps(data), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Order.objects.count(), 1)
        order = Order.objects.last()
        self.assertEqual(order.total_price, 1000)  # 4 * 100 + 3 * 200
        self.assertEqual(order.items_sizes.count(), 2)

    def test_update_order_status(self):
        order = OrderFactory(restaurant=self.restaurant, status=1)

        url = reverse("api_v1:orders-status", kwargs={"restaurant_id": self.restaurant.pk, "pk": order.pk})
        self.assertEqual(order.cooked_at, None)
        self.assertEqual(order.status, 1)

        response = self.client.post(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        order.refresh_from_db()
        self.assertEqual(order.status, 2)
        self.assertNotEqual(order.cooked_at, None)
        self.assertEqual(order.ready_at, None)

        response = self.client.post(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        order.refresh_from_db()
        self.assertEqual(order.status, 3)
        self.assertNotEqual(order.ready_at, None)
        self.assertEqual(order.on_the_way_at, None)

        response = self.client.post(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        order.refresh_from_db()
        self.assertEqual(order.status, 4)
        self.assertNotEqual(order.ready_at, None)
        self.assertEqual(order.delivered_at, None)

        response = self.client.post(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        order.refresh_from_db()
        self.assertEqual(order.status, 5)
        self.assertNotEqual(order.delivered_at, None)

        response = self.client.post(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        order.refresh_from_db()
        self.assertEqual(order.status, 5)

    def test_cancel_order(self):
        order = OrderFactory(restaurant=self.restaurant, status=1)

        url = reverse("api_v1:orders-status", kwargs={"restaurant_id": self.restaurant.pk, "pk": order.pk})
        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        order.refresh_from_db()
        self.assertEqual(order.status, 6)

    def test_cannot_cancel_order(self):
        order = OrderFactory(restaurant=self.restaurant, status=4)

        url = reverse("api_v1:orders-status", kwargs={"restaurant_id": self.restaurant.pk, "pk": order.pk})
        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        order.refresh_from_db()
        self.assertEqual(order.status, 4)
        self.assertEqual(response.json().get('errors'), "Can't cancel this order")

    def test_delete_order(self):
        order = OrderFactory(restaurant=self.restaurant)
        url = reverse("api_v1:orders-detail", kwargs={"restaurant_id": self.restaurant.pk, "pk": order.pk})

        self.assertEqual(Order.objects.count(), 1)
        response = self.client.delete(url, content_type='application/json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Order.objects.count(), 0)

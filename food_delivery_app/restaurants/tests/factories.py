import factory

from food_delivery_app.users.tests.factories import UserFactory

from ..models import Restaurant, Category, ItemSize, Item, ItemSizeDetails, Order, ItemOrderDetails


class RestaurantFactory(factory.django.DjangoModelFactory):
    owner = factory.SubFactory(UserFactory)
    name = factory.Faker('name')
    phone = factory.Faker('phone_number')
    address = factory.Faker('address')

    class Meta:
        model = Restaurant

    @factory.post_generation
    def users(self, create, users, **kwargs):
        if not create:
            return
        if users:
            for user in users:
                self.users.add(user)


class CategoryFactory(factory.django.DjangoModelFactory):
    restaurant = factory.SubFactory(RestaurantFactory)
    name = factory.Sequence(lambda n: 'category-{0}'.format(n))

    class Meta:
        model = Category


class ItemSizeFactory(factory.django.DjangoModelFactory):
    restaurant = factory.SubFactory(RestaurantFactory)
    name = factory.Sequence(lambda n: 'meduim-{0}'.format(n))

    class Meta:
        model = ItemSize


class ItemFactory(factory.django.DjangoModelFactory):
    restaurant = factory.SubFactory(RestaurantFactory)
    category = factory.SubFactory(CategoryFactory)
    sizes = factory.SubFactory(ItemSizeFactory)
    name = factory.Faker('name')
    short_description = factory.Faker('sentence', nb_words=4)

    class Meta:
        model = Item

    @factory.post_generation
    def sizes(self, create, sizes, **kwargs):
        if not create:
            return
        if sizes:
            for size in sizes:
                self.sizes.add(size)


class ItemSizeDetailsFactory(factory.django.DjangoModelFactory):
    item = factory.SubFactory(ItemFactory)
    size = factory.SubFactory(ItemSizeFactory)
    price = factory.Faker('random_int', min=10, max=1000)

    class Meta:
        model = ItemSizeDetails


class OrderFactory(factory.django.DjangoModelFactory):
    customer = factory.SubFactory(UserFactory)
    restaurant = factory.SubFactory(RestaurantFactory)
    address = factory.Faker('address')
    status = factory.Faker('random_element', elements=[status[0] for status in Order.STATUS_CHOICES])

    class Meta:
        model = Order

    @factory.post_generation
    def item_sizes(self, create, item_sizes, **kwargs):
        if not create:
            return
        if item_sizes:
            for item_size in item_sizes:
                self.item_sizes.add(item_size)


class ItemOrderDetailsFactory(factory.django.DjangoModelFactory):
    item_size = factory.SubFactory(ItemSizeDetailsFactory)
    order = factory.SubFactory(OrderFactory)
    count = factory.Faker('random_int', min=1, max=10)

    class Meta:
        model = ItemOrderDetails


def create_item_with_sizes(restaurant, number_of_sizes=1):
    item = ItemFactory(restaurant=restaurant)
    for _ in range(number_of_sizes):
        item_size = ItemSizeFactory(restaurant=restaurant)
        ItemSizeDetailsFactory(item=item, size=item_size)
    return item

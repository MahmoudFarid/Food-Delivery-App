import factory
from django.contrib.auth import get_user_model

User = get_user_model()


class UserFactory(factory.django.DjangoModelFactory):
    username = factory.Faker('user_name')
    email = factory.Sequence(lambda n: 'user-{0}@example.com'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'password')
    first_name = factory.Faker('name')
    last_name = factory.Faker('name')
    name = factory.Faker('name')
    address = factory.Faker('address')

    is_staff = False
    is_active = True

    class Meta:
        model = User
        django_get_or_create = ('email',)

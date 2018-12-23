from django.apps import AppConfig


class RestaurantsConfig(AppConfig):
    name = 'food_delivery_app.restaurants'

    def ready(self):
        from . import signals

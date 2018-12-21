from django.urls import include, path

from rest_framework.routers import DefaultRouter

router_v1 = DefaultRouter('v1')

urlpatterns = [
    path('restaurants/', include('food_delivery_app.restaurants.routers')),

] + router_v1.urls

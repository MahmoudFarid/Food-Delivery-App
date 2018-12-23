from rest_framework.routers import DefaultRouter

from .views import RestaurantViewSet, ItemSizeViewSet, CategoryViewSet, ItemViewSet, OrderViewSet

router_v1 = DefaultRouter()
router_v1.register('', RestaurantViewSet, base_name='restaurants'),
router_v1.register('(?P<restaurant_id>\d+)/item_sizes', ItemSizeViewSet, base_name='item_sizes'),
router_v1.register('(?P<restaurant_id>\d+)/categories', CategoryViewSet, base_name='categories'),
router_v1.register('(?P<restaurant_id>\d+)/items', ItemViewSet, base_name='items'),
router_v1.register('(?P<restaurant_id>\d+)/orders', OrderViewSet, base_name='orders'),
urlpatterns = router_v1.urls

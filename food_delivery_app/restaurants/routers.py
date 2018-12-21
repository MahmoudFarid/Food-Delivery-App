from rest_framework.routers import DefaultRouter

from .views import RestaurantViewSet

router_v1 = DefaultRouter()
router_v1.register('', RestaurantViewSet, base_name='restaurants'),
urlpatterns = router_v1.urls

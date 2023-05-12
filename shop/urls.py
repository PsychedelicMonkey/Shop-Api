from rest_framework import routers
from .views import OrderViewSet, ProductViewSet, ReviewViewSet

router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet, basename="orders")
router.register(r'products', ProductViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = router.urls

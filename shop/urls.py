from rest_framework import routers
from .views import OrderViewSet, ProductViewSet

router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet, basename="orders")
router.register(r'products', ProductViewSet)

urlpatterns = router.urls

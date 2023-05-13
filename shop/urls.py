from rest_framework import routers
from .views import OrderViewSet, ProductViewSet, ProductReviews, ReviewViewSet

router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet, basename="orders")
router.register(r'product-reviews', ProductReviews, basename="product-reviews")
router.register(r'products', ProductViewSet)
router.register(r'reviews', ReviewViewSet)

urlpatterns = router.urls

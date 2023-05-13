from rest_framework import routers
from .views import OrderViewSet, ProductViewSet, ProductReviews, ReviewViewSet

router = routers.DefaultRouter()
router.register(r'orders', OrderViewSet, basename="orders")
router.register(r'product-reviews', ProductReviews, basename="product-reviews")
router.register(r'products', ProductViewSet, basename="products")
router.register(r'reviews', ReviewViewSet, basename="reviews")

urlpatterns = router.urls

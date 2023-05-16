from django.shortcuts import render
from rest_framework import permissions, viewsets
from rest_framework.response import Response
from .models import Product, Review
from .permissions import IsAdminOrReadOnly
from .serializers import ProductSerializer, ProductReviewSerializer, ReviewSerializer


class ProductViewSet(viewsets.ModelViewSet):
    """
    View all products
    Permissions: Non-admin users have read-only permissions

    GET /api/products/
    GET /api/products/{product-slug}
    """

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    lookup_field = 'slug'


class ProductReviews(viewsets.GenericViewSet):
    """
    Retrieve all reviews for a given product

    GET /api/product-reviews/{product-id}
    """

    queryset = Review.objects.all()

    serializer_class = ProductReviewSerializer

    def retrieve(self, request, pk=None):
        queryset = Review.objects.filter(product=pk).order_by('-created_at')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """
    Retrieve all reviews created by the currently signed-in user
    """

    serializer_class = ReviewSerializer

    permission_classes = [
        permissions.IsAuthenticated,
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return self.request.user.reviews.all()

from django.shortcuts import render
from rest_framework import permissions, viewsets
from .models import Product, Review
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly
from .serializers import OrderSerializer, ProductSerializer, ReviewSerializer


class OrderViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post', 'head']

    serializer_class = OrderSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_queryset(self):
        return self.request.user.orders.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()

    serializer_class = ProductSerializer

    permission_classes = [IsAdminOrReadOnly]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()

    serializer_class = ReviewSerializer

    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

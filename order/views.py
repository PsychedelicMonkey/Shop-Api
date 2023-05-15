from django.shortcuts import render
from rest_framework import permissions, viewsets
from .serializers import OrderSerializer


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


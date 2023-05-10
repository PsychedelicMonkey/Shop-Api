from django.shortcuts import render
from knox.models import AuthToken
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import LoginSerializer, RegisterSerializer, UserSerializer


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response({
            'token': AuthToken.objects.create(user)[1],
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
        })


class RegisterAPI(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'token': AuthToken.objects.create(user)[1],
            'user': UserSerializer(user, context=self.get_serializer_context()).data,
        })


class UserAPI(generics.RetrieveAPIView):
    serializer_class = UserSerializer

    permission_classes = [
        permissions.IsAuthenticated
    ]

    def get_object(self):
        return self.request.user

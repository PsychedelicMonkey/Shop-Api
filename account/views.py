from django.shortcuts import render
from django.contrib.auth.models import update_last_login
from knox.models import AuthToken
from rest_framework import generics, permissions
from rest_framework.response import Response
from .serializers import LoginSerializer, UserSerializer


class LoginAPI(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        update_last_login(None, user)
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

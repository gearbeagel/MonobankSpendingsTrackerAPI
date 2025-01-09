import os
import time
import hmac
import hashlib
import base64

from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
import requests

from .serializers import UserSerializer


class MainView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        if request.user.is_authenticated:
            return Response({'message': 'Hello World!'})
        else:
            auth_links = {
                'register': '/api/register/',
                'login': '/api/login/',
            }
            return Response({
                'message': 'Hello, please log in or register.',
                'auth_links': auth_links
            })


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(
                {"detail": "User created successfully"},
                status=status.HTTP_201_CREATED
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"error": "Credentials are invalid."}, status=status.HTTP_400_BAD_REQUEST)
        login(request, user)
        return Response({"detail": "User logged in."}, status=status.HTTP_200_OK)


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"detail": "User logged out."}, status=status.HTTP_200_OK)

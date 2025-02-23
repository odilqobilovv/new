from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.permissions import IsUsingRegisteredDevice




class TestAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You are using your registered device."})

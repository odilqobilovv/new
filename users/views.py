from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema, OpenApiExample
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.permissions import IsUsingRegisteredDevice
from users.serializers import RegisterSerializer, LoginSerializer, RefreshTokenSerializer


class RegisterAPIView(APIView):
    @extend_schema(
        tags=["auth"],
        request=RegisterSerializer,
        # examples=[
        #     OpenApiExample(
        #         name="Example of Request",
        #         value={
        #             'username': 'Jhon',
        #             'email': 'example@gmail.com',
        #             'password': 'qwertyuiop'
        #         },
        #         description="Example of a user registration request"
        #     )
        # ]
    )
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": serializer.data,
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    @extend_schema(
        tags=["auth"],
        request=LoginSerializer,
        # examples=[
        #     OpenApiExample(
        #         name="Example of Login Request",
        #         value={
        #             'username': 'Jhon',
        #             'password': 'qwertyuiop'
        #         },
        #         description="Example of a user login request"
        #     )
        # ]
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    return Response({"error": "User account is inactive."}, status=status.HTTP_401_UNAUTHORIZED)
                refresh = RefreshToken.for_user(user)
                return Response({
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                }, status=status.HTTP_200_OK)
            return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RefreshTokenAPIView(APIView):
    @extend_schema(
        tags=["auth"],
        request=RefreshTokenSerializer,
        examples=[
            OpenApiExample(
                name="Example of Refresh Access Token Request",
                value={
                    'refresh': "asdfgtresdcvbnjytrdfbhjyw4567uythgfd"
                },
                description="Example of a user get another access token request"
            )
        ]
    )
    def post(self, request):
        serializer = RefreshTokenSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                "access": serializer.validated_data["access"]
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TestAPIView(APIView):
    permission_classes = [IsAuthenticated, IsUsingRegisteredDevice]

    def get(self, request):
        return Response({"message": "You are using your registered device."})
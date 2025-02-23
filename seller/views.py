from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError, PermissionDenied
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.serializers import LoginSerializer
from seller.models.products import Product, Review
from seller.serializers import ProductsSerializer


class SellerLoginAPIView(APIView):
    permission_classes = [AllowAny]
    @extend_schema(
        request=LoginSerializer,
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)

            if user:
                if user.user_type != 'vendor':  # Ensure only sellers can log in
                    return Response({"error": "Only sellers can log in."}, status=status.HTTP_403_FORBIDDEN)
                if not user.is_active:
                    return Response({"error": "Seller account is inactive."}, status=status.HTTP_401_UNAUTHORIZED)

                refresh = RefreshToken.for_user(user)
                return Response({
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                }, status=status.HTTP_200_OK)

            return Response({"error": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductCreateAPIView(APIView):
    @extend_schema(request=ProductsSerializer)
    def post(self, request):
        serializer = ProductsSerializer(data=request.data)
        if serializer.is_valid():
            product = serializer.save()
            return Response(ProductsSerializer(product).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductUpdateAPIView(APIView):
    @extend_schema(request=ProductsSerializer)
    def patch(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        serializer = ProductsSerializer(product, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductsAPIView(generics.ListAPIView):
    serializer_class = ProductsSerializer
    queryset = Product.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.user_type == 'vendor':
            raise PermissionDenied("You are not a vendor and cannot access this view.")

        return Product.objects.filter(seller=user)
from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework import generics, permissions, status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from apps.users.models.orders import Order, OrderItem
from apps.users.serializers import ProductDataSerializer, CategoryDataSerializer, ShopSerializer, RegisterSerializer, \
    LoginSerializer, RefreshTokenSerializer, UserRegistrationSerializer
from seller.models.shop import Shop
from seller.models.category import Category
from seller.models.products import Product
from seller.models.products import Review
from seller.serializers import OrderSerializer, OrderItemSerializer, ReviewSerializer, ProductsSerializer



@extend_schema(request=UserRegistrationSerializer, tags=['user-auth'])
class UserRegistrationAPIView(APIView):
    permission_classes = []
    authentication_classes = []
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Your request has been sent to the admin for approval.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@extend_schema(request=LoginSerializer, tags=['user-auth'])
class LoginAPIView(APIView):
    permission_classes = []
    authentication_classes = []
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)

        if user is None:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

        if not user.is_approved:
            return Response({'error': 'Your account is not approved yet. Please wait for admin approval.'},
                            status=status.HTTP_403_FORBIDDEN)

        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh_token': str(refresh),
            'access_token': str(refresh.access_token),
        })




@extend_schema(request=OrderSerializer)
class OrderListCreateView(generics.ListCreateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)

@extend_schema(request=OrderSerializer)
class OrderDetailView(generics.RetrieveDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(customer=self.request.user)

@extend_schema(request=OrderItemSerializer)
class OrderItemCreateView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(customer=request.user)
        serializer = OrderItemSerializer(data=request.data)

        if serializer.is_valid():
            product = serializer.validated_data['product']
            quantity = serializer.validated_data['product_quantity']

            if quantity > product.amount:
                raise ValidationError(f"Not enough stock available. Maximum: {product.amount}")

            order_item = OrderItem.objects.create(order=order, product=product, product_quantity=quantity)
            product.amount -= quantity
            product.save()
            order.update_total_price()

            return Response(OrderSerializer(order).data)

        return Response(serializer.errors, status=400)


@extend_schema(request=ReviewSerializer)
class ReviewListCreateView(generics.ListCreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema(request=ProductDataSerializer)
class ProductsGetAPIView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductsSerializer
    filter_backends = (SearchFilter, )
    search_fields = ['name_ru', 'name_uz', 'articul']

@extend_schema(request=CategoryDataSerializer)
class CategoryGetAPIView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDataSerializer
    filter_backends = (SearchFilter,)
    search_fields = ['name_ru', 'name_uz']

class ProductDetailAPIView(generics.RetrieveAPIView):
    serializer_class = ProductsSerializer

    def get_queryset(self):
        articul = self.kwargs.get('articul')
        try:
            return Product.objects.filter(articul=articul)
        except Product.DoesNotExist:
            raise NotFound("Product with this articl not found.")

    def get_object(self):
        queryset = self.get_queryset()
        if queryset.exists():
            return queryset.first()
        raise NotFound("Product with this articl not found.")


class CategoryDetailAPIView(generics.RetrieveAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryDataSerializer


class ShopAPIView(generics.RetrieveAPIView):
    queryset = Shop.objects.all()
    serializer_class = ShopSerializer


    def get_queryset(self):
        name = self.kwargs.get('name')
        try:
            return Shop.objects.filter(name=name)
        except Shop.DoesNotExist:
            raise NotFound("Shop with this name not found.")

    def get_object(self):
        queryset = self.get_queryset()
        if queryset.exists():
            return queryset.first()
        raise NotFound("Shop with this name not found.")


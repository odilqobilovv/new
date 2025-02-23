from drf_spectacular.utils import extend_schema
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions

from seller.models.products import Product, Review
from seller.serializers import ProductsSerializer, ReviewSerializer, OrderSerializer, OrderItemSerializer
from seller.models.orders import Order, OrderItem

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
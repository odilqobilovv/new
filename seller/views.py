from drf_spectacular.utils import extend_schema
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from seller.models import Product
from seller.serializers import ProductsSerializer



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

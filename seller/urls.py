from django.urls import path

from seller.views import ProductCreateAPIView, ProductUpdateAPIView, ProductsAPIView, SellerLoginAPIView

urlpatterns = [
    path('login/', SellerLoginAPIView.as_view()),
    path('product/create/' ,ProductCreateAPIView.as_view()),
    path('product/update/<int:pk>/', ProductUpdateAPIView.as_view()),
    path('products/', ProductsAPIView.as_view()),
]
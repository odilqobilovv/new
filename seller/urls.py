from django.urls import path

from seller.views import ProductCreateAPIView, ProductUpdateAPIView

urlpatterns = [
    path('product/create/' ,ProductCreateAPIView.as_view()),
    path('product/update/<int:pk>/', ProductUpdateAPIView.as_view()),
]
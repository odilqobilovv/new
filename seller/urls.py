from django.urls import path

from seller.views import ProductCreateAPIView, ProductUpdateAPIView, OrderListCreateView, OrderDetailView, \
    OrderItemCreateView, ReviewListCreateView

urlpatterns = [
    path('product/create/' ,ProductCreateAPIView.as_view()),
    path('product/update/<int:pk>/', ProductUpdateAPIView.as_view()),
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/add-item/', OrderItemCreateView.as_view(), name='order-item-create'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
]
from django.urls import path

from apps.users.views import OrderListCreateView, OrderDetailView, OrderItemCreateView, ReviewListCreateView, \
    ProductsGetAPIView, CategoryGetAPIView, ProductDetailAPIView, CategoryDetailAPIView, ShopAPIView, \
    UserRegistrationAPIView, LoginAPIView

urlpatterns = [
    # auth
    path('register/', UserRegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    # orders
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),
    path('orders/add-item/', OrderItemCreateView.as_view(), name='order-item-create'),
    path('reviews/', ReviewListCreateView.as_view(), name='review-list-create'),
    # products
    path('products/', ProductsGetAPIView.as_view()),
    path('product/<int:articul>/', ProductDetailAPIView.as_view()),
    path('categories/', CategoryGetAPIView.as_view()),
    path('category/<int:pk>/', CategoryDetailAPIView.as_view()),
    # shop
    path('shop/<str:name>/', ShopAPIView.as_view()),
]
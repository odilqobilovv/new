from django.urls import path

from accounts.views import LoginAPIView, RegisterAPIView, RefreshTokenAPIView, TestAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('token/refresh/', RefreshTokenAPIView.as_view()),
    path('test/', TestAPIView.as_view()),
]
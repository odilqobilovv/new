from django.urls import path

from apps.admins.views import PendingUsersListView, ApproveUserView, AdminLoginAPIView

urlpatterns = [
    path('login/', AdminLoginAPIView.as_view()),
    path('users/pending/', PendingUsersListView.as_view()),
    path('users/approve/<int:pk>/', ApproveUserView.as_view()),
]
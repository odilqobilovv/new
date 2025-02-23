from django.contrib.auth import authenticate
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User
from apps.users.serializers import UserRegistrationSerializer, LoginSerializer
from root.permissions import IsAdminUserCustom


class AdminLoginAPIView(APIView):
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

            if user and user.user_type == 'admin':
                if not user.is_active:
                    return Response({"error": "Admin account is inactive."}, status=status.HTTP_401_UNAUTHORIZED)

                refresh = RefreshToken.for_user(user)
                return Response({
                    "access_token": str(refresh.access_token),
                    "refresh_token": str(refresh),
                }, status=status.HTTP_200_OK)

            return Response({"error": "Invalid credentials or not an admin."}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@extend_schema(request=UserRegistrationSerializer)
class PendingUsersListView(ListAPIView):
    # queryset = User.objects.filter(is_approved=False, user_type='user')
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsAdminUserCustom]

    def get_queryset(self):
        return User.objects.filter(is_approved=False, user_type="user")

@extend_schema(request=UserRegistrationSerializer)
class ApproveUserView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [IsAdminUserCustom]

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        user.is_approved = True
        user.save()
        return Response({'message': 'User has been approved successfully.'})

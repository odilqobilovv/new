from django.contrib.auth import get_user_model
from rest_framework import serializers

from seller.models import Category, Shop
from seller.models.products import Product

from rest_framework import serializers
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from accounts.models import User


class ProductDataSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ("name_ru", "name_uz", "price", "description_uz", "description_ru", "category", "articul", "shop")
        model = Product

class CategoryDataSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Category

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        fields = "__all__"
        model = Shop



class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'phone', 'password', 'payment_method')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            phone=validated_data.get('phone', ''),
            payment_method=validated_data.get('payment_method', '')
        )

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)


class RefreshTokenSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        refresh_token = attrs.get("refresh")
        try:
            token = RefreshToken(refresh_token)
            attrs["access"] = str(token.access_token)
        except TokenError:
            raise serializers.ValidationError("Invalid refresh token.")
        return attrs



User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta:
        model = User
        fields = ['id','username', 'email', 'password', 'payment_method']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data, is_approved=False)  # User must be approved by admin
        return user
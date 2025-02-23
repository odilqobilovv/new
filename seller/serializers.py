from rest_framework import serializers

from seller.models.products import Product, PhotoProducts, VideoProducts, KeywordsProduct, CharacteristicsProduct, \
    ProductVariant
from seller.models.orders import Order, OrderItem
from seller.models.products import Review


class PhotoProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = PhotoProducts
        fields = ['id', 'image']

class VideoProductsSerializer(serializers.ModelSerializer):
    class Meta:
        model = VideoProducts
        fields = ['id', 'video']

class KeywordsProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = KeywordsProduct
        fields = ['id', 'keyword']

class CharacteristicsProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = CharacteristicsProduct
        fields = ['id', 'title_uz', 'title_ru', 'info_uz', 'info_ru']

class ProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ['id', 'color', 'size', 'stock', 'price', 'discount']

class ProductsSerializer(serializers.ModelSerializer):
    photos = PhotoProductsSerializer(many=True, required=False)
    videos = VideoProductsSerializer(many=True, required=False)
    product_keywords = KeywordsProductSerializer(many=True, required=False)
    characteristics = CharacteristicsProductSerializer(many=True, required=False)
    variants = ProductVariantSerializer(many=True, required=False)
    articul = serializers.CharField(read_only=True, required=False)

    class Meta:
        model = Product
        fields = "__all__"

    def create(self, validated_data):
        photos_data = validated_data.pop('photos', [])
        videos_data = validated_data.pop('videos', [])
        keywords_data = validated_data.pop('product_keywords', [])
        characteristics_data = validated_data.pop('characteristics', [])
        variants_data = validated_data.pop('variants', [])

        # Asosiy mahsulotni yaratish
        product = Product.objects.create(**validated_data)

        # Related model ma'lumotlarini yaratish
        for photo in photos_data:
            PhotoProducts.objects.create(product=product, **photo)

        for video in videos_data:
            VideoProducts.objects.create(product=product, **video)

        for keyword in keywords_data:
            KeywordsProduct.objects.create(product=product, **keyword)

        for characteristic in characteristics_data:
            CharacteristicsProduct.objects.create(product=product, **characteristic)

        for variant in variants_data:
            ProductVariant.objects.create(product=product, **variant)

        return product

    def update(self, instance, validated_data):
        photos_data = validated_data.pop('photos', [])
        videos_data = validated_data.pop('videos', [])
        keywords_data = validated_data.pop('product_keywords', [])
        characteristics_data = validated_data.pop('characteristics', [])
        variants_data = validated_data.pop('variants', [])

        # Asosiy maydonlarni yangilash
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Eski ma'lumotlarni o'chirish
        instance.photos.all().delete()
        instance.videos.all().delete()
        instance.product_keywords.all().delete()
        instance.characteristics.all().delete()
        instance.variants.all().delete()

        # Yangi ma'lumotlarni qo'shish
        for photo in photos_data:
            PhotoProducts.objects.create(product=instance, **photo)

        for video in videos_data:
            VideoProducts.objects.create(product=instance, **video)

        for keyword in keywords_data:
            KeywordsProduct.objects.create(product=instance, **keyword)

        for characteristic in characteristics_data:
            CharacteristicsProduct.objects.create(product=instance, **characteristic)

        for variant in variants_data:
            ProductVariant.objects.create(product=instance, **variant)

        return instance


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'product_quantity', 'price_per_unit']
        read_only_fields = ['price_per_unit']

    def validate(self, data):
        product = data['product']
        quantity = data['product_quantity']

        if quantity > product.amount:
            raise serializers.ValidationError(f"Not enough stock available. Maximum available: {product.amount} units.")

        return data


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'total_price', 'order_items']
        read_only_fields = ['total_price']

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        order = Order.objects.create(customer=user)

        return order


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'user', 'product', 'rating', 'comment', 'created_at']
        read_only_fields = ['user']

    def validate(self, data):
        user = self.context['request'].user
        product = data['product']

        if not OrderItem.objects.filter(order__customer=user, product=product).exists():
            raise serializers.ValidationError("You can only review products you have purchased.")

        return data

    def create(self, validated_data):
        review = super().create(validated_data)
        review.product.update_rating()
        return review

import random

from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from django.db import models

from seller.models.category import Category
from seller.models.shop import Shop
from accounts.models.user import User


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Product(BaseModel):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name_ru = models.CharField(max_length=255)
    name_uz = models.CharField(max_length=255)
    description_ru = models.CharField(max_length=255)
    description_uz = models.CharField(max_length=255)
    price = models.IntegerField()
    amount = models.IntegerField()
    min_sell = models.PositiveIntegerField(default=1)
    articul = models.CharField(max_length=8, unique=True, validators=[RegexValidator(r'^\d{8}$', 'Artikule must consist of 8 digits.')], blank=True)

    rating = models.FloatField(default=0.0)

    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='category')

    def save(self, *args, **kwargs):
        if not self.articul:
            self.articul = self.generate_articul()
        super().save(*args, **kwargs)


    def update_rating(self):
        reviews = self.reviews.all()
        total_reviews = reviews.count()
        if total_reviews > 0:
            self.rating = sum(review.rating for review in reviews) / total_reviews
        else:
            self.rating = 0.0
        self.save()

    def get_price_for_quantity(self, quantity):
        bulk_prices = self.bulk_prices.filter(min_quantity__lte=quantity).order_by('-min_quantity')
        if bulk_prices.exists():
            return bulk_prices.first().price_per_unit  # Get the best bulk price
        return self.price

    @staticmethod
    def generate_articul():
        while True:
            articul = str(random.randint(10000000, 99999999))
            if not Product.objects.filter(articul=articul).exists():
                return articul

    def __str__(self):
        return f'{self.name_ru} | {self.shop.name}'


class ProductVariant(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants", blank=True, null=True)
    color = models.CharField(max_length=50, blank=True, null=True)
    size = models.CharField(max_length=50, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount = models.DecimalField(max_digits=5, decimal_places=2, default=0, help_text="Discount in percentage")
    min_sell = models.PositiveIntegerField(default=1)


    def __str__(self):
        return f"{self.product.name_uz} - {self.color} - {self.size}"


class BulkPrice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="bulk_prices")
    min_quantity = models.PositiveIntegerField()
    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        ordering = ['min_quantity']

    def __str__(self):
        return f'{self.min_quantity}+ units for ${self.price_per_unit} each'



class KeywordsProduct(BaseModel):
    keyword = models.CharField(max_length=55, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="product_keywords", blank=True, null=True)
    product_variants = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="variant_keywords", blank=True, null=True)

    def __str__(self):
        return self.keyword


class PhotoProducts(BaseModel):
    image = models.ImageField(upload_to='products/images/', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='photos', blank=True, null=True)
    product_variants = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="variant_photos", blank=True, null=True)

class VideoProducts(BaseModel):
    video = models.FileField(upload_to='products/videos/', blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='videos', blank=True, null=True)
    product_variants = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="variant_videos", blank=True, null=True)

class CharacteristicsProduct(BaseModel):
    title_uz = models.CharField(max_length=75)
    title_ru = models.CharField(max_length=75)
    info_uz = models.CharField(max_length=255)
    info_ru = models.CharField(max_length=255)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='characteristics', blank=True, null=True)
    # product_variants = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name="variant_characteristics", blank=True, null=True)

    def __str__(self):
        return f"{self.title_uz} | {self.title_ru}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'product')

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.product.update_rating()

    def delete(self, *args, **kwargs):
        super().delete(*args, **kwargs)
        self.product.update_rating()

    def __str__(self):
        return f"{self.user.username} - {self.product.name_ru} ({self.rating} stars)"

from django.contrib import admin


from seller.models.products import Product, ProductVariant, KeywordsProduct, PhotoProducts, VideoProducts, \
    CharacteristicsProduct, BulkPrice

from seller.models import Category
from seller.models.products import Review
from seller.models.orders import Order, OrderItem
from seller.models.shop import Shop


admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(Shop)
admin.site.register(Review)

class PhotoProductsInline(admin.TabularInline):
    model = PhotoProducts
    extra = 1

class VideoProductsInline(admin.TabularInline):
    model = VideoProducts
    extra = 1

class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1

class KeywordsInline(admin.TabularInline):
    model = KeywordsProduct
    extra = 1

class CharacteriticsInline(admin.TabularInline):
    model = CharacteristicsProduct
    extra = 1

class BulkPriceInline(admin.TabularInline):
    model = BulkPrice
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name_ru", "name_uz", "amount")
    search_fields = ("name_ru", "name_uz")
    inlines = [PhotoProductsInline, VideoProductsInline, ProductVariantInline, KeywordsInline, CharacteriticsInline, BulkPriceInline]


@admin.register(ProductVariant)
class ProductVariantAdmin(admin.ModelAdmin):
    list_display = ("get_name_ru", "get_name_uz", "get_sold", "get_amount")
    search_fields = ("product__name_ru", "product__name_uz", "optom_product__name_ru", "optom_product__name_uz")

    inlines = [PhotoProductsInline, VideoProductsInline, KeywordsInline]

    def get_name_ru(self, obj):
        return obj.product.name_ru if obj.product else obj.optom_product.name_ru if obj.optom_product else "-"

    def get_name_uz(self, obj):
        return obj.product.name_uz if obj.product else obj.optom_product.name_uz if obj.optom_product else "-"

    def get_sold(self, obj):
        return obj.product.sold if obj.product else obj.optom_product.sold if obj.optom_product else False

    def get_amount(self, obj):
        return obj.product.amount if obj.product else obj.optom_product.amount if obj.optom_product else 0

    get_name_ru.short_description = "Name RU"
    get_name_uz.short_description = "Name UZ"
    get_sold.short_description = "Sold"
    get_amount.short_description = "Amount"



@admin.register(KeywordsProduct)
class KeywordsProductAdmin(admin.ModelAdmin):
    list_display = ("keyword", "product")

@admin.register(PhotoProducts)
class PhotoProductsAdmin(admin.ModelAdmin):
    list_display = ("product", "image")

@admin.register(VideoProducts)
class VideoProductsAdmin(admin.ModelAdmin):
    list_display = ("product", "video")

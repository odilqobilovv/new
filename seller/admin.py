from django.contrib import admin

from seller.models import Category
from seller.models.products import Product, Comment, Suplier
from seller.models.orders import Order, OrderItem
from seller.models.shop import Shop

# Register your models here.

admin.site.register(Product)
admin.site.register(Order)
admin.site.register(Shop)
admin.site.register(OrderItem)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Suplier)
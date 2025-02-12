from django.db import models

from apps.users.models import User


class Shop(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return f'{self.owner} | {self.name}'

class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.IntegerField()
    amount = models.IntegerField()
    supplier = models.CharField(max_length=255)
    supplier_phone = models.IntegerField()
    bulk_amount = models.PositiveIntegerField(default=10)

    def __str__(self):
        return f'{self.name} | {self.shop.name}'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.IntegerField(default=0)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    packs = models.IntegerField()

    def save(self, *args, **kwargs):
        total_quantity = self.packs * self.product.bulk_amount
        if total_quantity > self.product.amount:
            raise ValueError(f"Not enough stock available. Maximum available: {self.product.stock // self.product.bulk_quantity} packs.")
        super().save(*args, **kwargs)
from django.db import models

from seller.models.products import Product
from users.models.user import User

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.IntegerField(default=0)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    packs = models.IntegerField()

    def save(self, *args, **kwargs):
        total_quantity = self.packs * self.product.bulk_amount
        if total_quantity > self.product.amount:
            raise ValueError(f"Not enough stock available. Maximum available: {self.product.stock // self.product.amount} packs.")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product.name

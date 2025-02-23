from django.db import models
from seller.models.products import Product
from accounts.models.user import User

class Order(models.Model):
    STATUS_CHOICES = [
        ('new', 'New'),
        ('pending', 'Pending'),
        ('delivered', 'Delivered'),
        ('declined', 'Declined'),
    ]
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')

    def update_total_price(self):
        total = sum(item.get_total_price() for item in self.order_items.all())
        self.total_price = total
        self.save()

    def __str__(self):
        return f"Order {self.id} - {self.customer}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    product_quantity = models.PositiveIntegerField()  # Now represents actual product amount

    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def save(self, *args, **kwargs):
        if self.product_quantity > self.product.amount:
            raise ValueError(f"Not enough stock available. Maximum available: {self.product.amount} units.")

        self.price_per_unit = self.product.get_price_for_quantity(self.product_quantity)

        super().save(*args, **kwargs)
        self.order.update_total_price()

    def get_total_price(self):
        return self.price_per_unit * self.product_quantity

    def __str__(self):
        return f"{self.product.name_ru} - {self.product_quantity} units"
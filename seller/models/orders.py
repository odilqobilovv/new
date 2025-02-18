from django.db import models
from seller.models.products import Product
from users.models.user import User

class Order(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def update_total_price(self):
        total = sum(item.get_total_price() for item in self.order_items.all())
        self.total_price = total
        self.save()

    def __str__(self):
        return f"Order {self.id} - {self.customer}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    packs = models.IntegerField()

    price_per_unit = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Add price_per_unit

    def save(self, *args, **kwargs):
        total_quantity = self.packs * self.product.min_sell

        # Check if the quantity exceeds the available stock
        if total_quantity > self.product.amount:
            raise ValueError(
                f"Not enough stock available. Maximum available: {self.product.amount // self.product.min_sell} packs.")

        # Get the price per unit based on total quantity
        self.price_per_unit = self.product.get_price_for_quantity(total_quantity)

        super().save(*args, **kwargs)  # Save the order item
        self.order.update_total_price()  # Update the total price of the order

    def get_total_price(self):
        return self.price_per_unit * self.packs * self.product.min_sell

    def __str__(self):
        return f"{self.product.name_ru} - {self.packs} packs"

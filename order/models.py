from django.contrib.auth.models import User
from django.db import models
from shop.models import Product


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    is_completed = models.BooleanField(default=False)
    date_shipped = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def total_price(self):
        return sum([item.product.price * item.quantity for item in self.items.all()])

    @property
    def num_items(self):
        return sum([item.quantity for item in self.items.all()])

    def __str__(self):
        return f'Order {self.pk} - {self.user.username}'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=False, blank=True)

from django.contrib import admin
from .models import Order, OrderItem, Product, ProductImage, Review


class OrderItemInline(admin.StackedInline):
    model = OrderItem


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    readonly_fields = ['width', 'height']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [OrderItemInline]
    readonly_fields = ['total_price', 'num_items']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(Review)

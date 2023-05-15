from django.contrib import admin
from .models import Product, ProductImage, Review


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    readonly_fields = ['width', 'height']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(Review)

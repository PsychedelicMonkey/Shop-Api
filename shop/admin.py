from django.contrib import admin
from .models import Product, ProductImage, Review


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields = ("img_preview", "image", "caption",)
    readonly_fields = ("img_preview",)
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(Review)

from django.contrib import admin
from .models import Product, ProductImage, Review


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields = ("img_tag", "image", "caption",)
    readonly_fields = ("img_tag",)
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ("name", "img_tag",)
    prepopulated_fields = {"slug": ["name"]}


admin.site.register(Review)

from django.contrib import admin
from .models import Category, Product, ProductImage, Review

admin.site.register(Category)
admin.site.register(Review)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields = ("img_tag", "image", "caption",)
    readonly_fields = ("img_tag",)
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    filter_horizontal = ("categories",)
    inlines = (ProductImageInline,)
    list_display_links = ("img_tag", "name",)
    list_display = ("img_tag", "name", "price",)
    list_filter = ("name", "price", "categories",)
    prepopulated_fields = {"slug": ["name"]}


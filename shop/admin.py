from django.contrib import admin
from .models import Category, Color, Product, ProductImage, ProductSize, Review, Size

admin.site.register(Category)
admin.site.register(Color)
admin.site.register(Review)
admin.site.register(Size)


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    fields = ("img_tag", "image", "caption", "color",)
    readonly_fields = ("img_tag",)
    extra = 0


class ProductSizeInline(admin.TabularInline):
    model = ProductSize
    extra = 0


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    filter_horizontal = ("categories", "colors",)
    inlines = (ProductImageInline, ProductSizeInline,)
    list_display_links = ("img_tag", "name",)
    list_display = ("img_tag", "name", "price",)
    list_filter = ("name", "price", "categories",)
    prepopulated_fields = {"slug": ["name"]}

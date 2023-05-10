from django.db import models
from PIL import Image


class Product(models.Model):
    name = models.CharField(max_length=125, null=False, blank=False)
    slug = models.SlugField(max_length=255, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=7, null=False, blank=False)
    quantity = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.name} ({self.pk})'


class ProductImage(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product", null=False, blank=False)
    caption = models.CharField(max_length=255, null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)

    def save(self, *args, **kwargs):
        super(ProductImage, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        width, height = img.size
        self.width = width
        self.height = height
        return super(ProductImage, self).save(*args, **kwargs)

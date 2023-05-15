from django.contrib.auth.models import User
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

    @property
    def review_score(self):
        try:
            score = sum([review.rating for review in self.reviews.all()])
            num = self.reviews.count()
            return score / num
        except ZeroDivisionError as e:
            return None

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


class Review(models.Model):
    class Rating(models.IntegerChoices):
        BAD = 1
        DISAPPOINTING = 2
        ALRIGHT = 3
        GOOD = 4
        AMAZING = 5

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(choices=Rating.choices, null=False, blank=False)
    body = models.TextField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Review: {self.product.name} - {self.user.username}'
    
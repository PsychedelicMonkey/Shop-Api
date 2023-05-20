from django.contrib.auth.models import User
from django.db import models
from django.utils.html import mark_safe
from PIL import Image


class Category(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("name",)
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name


class Color(models.Model):
    color = models.CharField(max_length=50, null=False, blank=False)

    class Meta:
        ordering = ("color",)

    def __str__(self):
        return self.color


class Product(models.Model):
    name = models.CharField(max_length=125, null=False, blank=False)
    slug = models.SlugField(max_length=255, null=False, blank=False, unique=True)
    description = models.TextField(null=True, blank=True)
    price = models.DecimalField(decimal_places=2, max_digits=7, null=False, blank=False)
    quantity = models.IntegerField(null=True, blank=True)
    categories = models.ManyToManyField(Category, blank=True)
    colors = models.ManyToManyField(Color, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @property
    def review_score(self):
        """
        Calculates the average review score for a product instance
        """

        try:
            score = sum([review.rating for review in self.reviews.all()])
            num = self.reviews.count()
            return score / num
        except ZeroDivisionError as e:
            return None

    @property
    def review_count(self):
        """
        Returns the total number of reviews for a product instance
        """

        return self.reviews.count()

    @staticmethod
    def get_product_count():
        """
        Returns the total number of products
        """

        return Product.objects.count()

    def img_tag(self):
        """
        Display preview image in admin site
        """

        try:
            img = mark_safe(f'<img src="{self.images.first().image.url}" alt="" width="80" />')
        except AttributeError:
            img = mark_safe('<img src="" alt="No image found" />')
        return img

    def __str__(self):
        return f'{self.name} ({self.pk})'


class ProductImage(models.Model):
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="product", null=False, blank=False)
    caption = models.CharField(max_length=255, null=True, blank=True)
    width = models.IntegerField(null=True, blank=True)
    height = models.IntegerField(null=True, blank=True)
    color = models.ForeignKey(Color, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        super(ProductImage, self).save(*args, **kwargs)
        img = Image.open(self.image.path)
        width, height = img.size
        self.width = width
        self.height = height
        return super(ProductImage, self).save(*args, **kwargs)

    def __str__(self):
        return f'Product image: {self.pk}'

    def img_tag(self):
        """
        Display preview image in admin site
        """

        return mark_safe(f'<img src="{self.image.url}" alt"{self.caption}" width="150" />')


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

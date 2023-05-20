from rest_framework import serializers
from account.serializers import UserSerializer
from .models import Category, Color, Product, ProductImage, Review, Size


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("name", "description",)


class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = '__all__'


class SizeSerializer(serializers.ModelSerializer):
    count = serializers.IntegerField()
    color = ColorSerializer(many=False, read_only=True)

    class Meta:
        model = Size
        fields = '__all__'


class ProductImageSerializer(serializers.ModelSerializer):
    color = ColorSerializer(many=False, read_only=True)

    class Meta:
        model = ProductImage
        fields = ('image', 'caption', 'width', 'height', 'color',)


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    colors = ColorSerializer(many=True, read_only=True)
    sizes = SizeSerializer(source="productsize_set", many=True, read_only=False)
    images = ProductImageSerializer(many=True, read_only=True)
    review_score = serializers.DecimalField(decimal_places=1, max_digits=2)

    class Meta:
        model = Product
        fields = '__all__'


class ProductReviewSerializer(serializers.ModelSerializer):
    """
    Serializer for the Review model without including product information
    """

    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Review
        fields = ('id', 'rating', 'body', 'user', 'created_at', 'updated_at')


class ReviewSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField(required=True, write_only=True)
    product = ProductSerializer(many=False, read_only=True)
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Review
        fields = '__all__'

    def validate(self, data):
        if self.context['request'].method == 'POST':
            if Review.objects.filter(user=self.context['request'].user, product=data['product_id']).exists():
                raise serializers.ValidationError('You have already reviewed this product')
        return data

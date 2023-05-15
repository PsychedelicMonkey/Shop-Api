from rest_framework import serializers
from account.serializers import UserSerializer
from .models import Product, ProductImage, Review


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image', 'caption', 'width', 'height',)


class ProductSerializer(serializers.ModelSerializer):
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

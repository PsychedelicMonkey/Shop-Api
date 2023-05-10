from rest_framework import serializers
from .models import Order, OrderItem, Product, ProductImage


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ('image', 'caption', 'width', 'height',)


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = '__all__'


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(many=False, read_only=True)
    product_id = serializers.IntegerField(required=True, write_only=True)

    class Meta:
        model = OrderItem
        fields = ('product', 'quantity', 'product_id')


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = ('id', 'is_completed', 'date_shipped', 'total_price', 'num_items', 'items',)
        extra_kwargs = {
            'id': {'read_only': True},
            'is_completed': {'read_only': True},
            'date_shipped': {'read_only': True},
        }

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        order = Order.objects.create(user=validated_data['user'])
        for item_data in items_data:
            product = Product.objects.get(pk=item_data['product_id'])
            OrderItem.objects.create(order=order, product=product, quantity=item_data['quantity'])
        return order

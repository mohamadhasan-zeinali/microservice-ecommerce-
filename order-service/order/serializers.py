from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='order:orders-detail')
    class Meta:
        model = Order
        fields = ['url', 'product_id', 'quantity', 'total_price', 'created_at']
        read_only_fields = ['total_price', 'created_at']

    def create(self, validated_data):
        order = Order(
            product_id=validated_data['product_id'],
            quantity=validated_data['quantity']
        )
        order.save()
        return order


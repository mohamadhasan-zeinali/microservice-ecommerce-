from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='order:orders-detail')

    class Meta:
        model = Order
        fields = '__all__'
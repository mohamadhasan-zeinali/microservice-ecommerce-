from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='product:products-detail')

    class Meta:
        model = Product
        fields = '__all__'
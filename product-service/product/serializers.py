from rest_framework import serializers
from .models import Product
from django.core.cache import cache


class ProductSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='product:products-detail')

    class Meta:
        model = Product
        fields = '__all__'

    def to_representation(self, instance):
        cache_key = f'product_{instance.pk}'
        serialized_data = cache.get(cache_key)
        if not serialized_data:
            serialized_data = super(ProductSerializer, self).to_representation(instance)
            cache.set(cache_key, serialized_data, 60 * 60 * 24 * 365)
        return serialized_data
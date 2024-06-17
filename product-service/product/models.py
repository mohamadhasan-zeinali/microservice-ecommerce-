from django.db import models
from django_jalali.db import models as jmodel
from django.utils import  timezone
from django.core.cache import cache


class Product(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='name')
    description = models.CharField(max_length=300, verbose_name='description')
    price = models.DecimalField(max_digits=15, decimal_places=3, verbose_name='price')
    stock = models.IntegerField(verbose_name='stock')
    created_at = jmodel.jDateTimeField(auto_now_add=timezone.now, null=True, verbose_name='created_time')
    status = models.BooleanField(default=True,  verbose_name='status')

    def save(self, *args, **kwargs):
        cache.delete(f'product_{self.pk}')
        super().save(*args, **kwargs)
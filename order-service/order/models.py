from django.db import models
from django_jalali.db import models as jmodel
from django.utils import  timezone
from .publisher import publish_order_created

class Order(models.Model):
    product_id = models.IntegerField(verbose_name='product_ordered')
    quantity = models.IntegerField(verbose_name='number_of_order')
    total_price = models.DecimalField(max_digits=15, decimal_places=3, verbose_name='total_price')
    created_at = jmodel.jDateTimeField(auto_now_add=timezone.now, verbose_name='created_time')

    # for total_price = quantity * product_price ( come from product service )

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        publish_order_created({
            'order_id': self.id,
            'product_id': self.product_id,
            'quantity': self.quantity
        })
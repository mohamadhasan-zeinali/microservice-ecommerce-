from django.db import models
from django_jalali.db import models as jmodel
from django.utils import timezone
from .publisher import publish_order_created
from .rabbitmq_config import get_rabbitmq_connection, get_rabbitmq_channel
import json
from decimal import Decimal


class Order(models.Model):
    product_id = models.IntegerField(verbose_name='product_ordered')
    quantity = models.IntegerField(verbose_name='number_of_order')
    total_price = models.DecimalField(max_digits=15, decimal_places=3, null=True, verbose_name='total_price')
    created_at = jmodel.jDateTimeField(auto_now_add=timezone.now, verbose_name='created_time')

    def save(self, *args, **kwargs):
        product_details = self.get_product_details(self.product_id)
        if product_details and 'price' in product_details:
            # Ensure the price is a valid Decimal
            self.total_price = Decimal(str(product_details['price'])) * Decimal(str(self.quantity))
        else:
            raise ValueError("Product details could not be fetched or missing 'price'")
        super().save(*args, **kwargs)
        publish_order_created({
            'order_id': self.id,
            'product_id': self.product_id,
            'quantity': self.quantity
        })

    def get_product_details(self, product_id):
        connection = get_rabbitmq_connection()
        channel = get_rabbitmq_channel(connection)
        response = None

        def on_response(ch, method, props, body):
            nonlocal response
            response = json.loads(body)
            channel.basic_ack(delivery_tag=method.delivery_tag)

        channel.queue_declare(queue='product_response_queue', durable=True)
        channel.basic_consume(queue='product_response_queue', on_message_callback=on_response, auto_ack=False)

        message = json.dumps({'product_id': product_id})
        channel.queue_declare(queue='product_request_queue', durable=True)
        channel.basic_publish(exchange='', routing_key='product_request_queue', body=message)

        while response is None:
            connection.process_data_events()

        connection.close()
        return response


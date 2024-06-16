# products/consumer.py
import json
import pika
import requests
from django.conf import settings
from .rabbitmq_config import get_rabbitmq_connection, get_rabbitmq_channel
from .models import Product


def callback(ch, method, properties, body):
    order_data = json.loads(body)
    product_id = order_data['product_id']

    # Fetch product details from the database
    product = Product.objects.get(id=product_id)
    product_details = {
        'id': product.id,
        'name': product.name,
        'price': product.price,
        # add other relevant details
    }

    # Send product details to the Order service
    order_update_url = f'http://order-service/api/orders/{order_data["order_id"]}/update/'
    response = requests.post(order_update_url, json=product_details)

    if response.status_code == 200:
        ch.basic_ack(delivery_tag=method.delivery_tag)
    else:
        # Handle failure to send product details
        pass


def start_consuming():
    connection = get_rabbitmq_connection()
    channel = get_rabbitmq_channel(connection)

    channel.queue_declare(queue='order_queue', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='order_queue', on_message_callback=callback)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    start_consuming()

# products/publisher.py
import json
from .rabbitmq_config import get_rabbitmq_connection, get_rabbitmq_channel
import pika


def publish_product_updated(product_data):
    connection = get_rabbitmq_connection()
    channel = get_rabbitmq_channel(connection)

    channel.queue_declare(queue='product_queue', durable=True)

    message = json.dumps(product_data)
    channel.basic_publish(
        exchange='',
        routing_key='product_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,
        )
    )

    connection.close()

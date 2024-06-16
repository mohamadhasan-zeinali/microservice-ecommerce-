# orders/publisher.py
import json
from .rabbitmq_config import get_rabbitmq_connection, get_rabbitmq_channel
import pika


def publish_order_created(order_data):
    connection = get_rabbitmq_connection()
    channel = get_rabbitmq_channel(connection)

    channel.queue_declare(queue='order_queue', durable=True)

    message = json.dumps(order_data)
    channel.basic_publish(
        exchange='',
        routing_key='order_queue',
        body=message,
        properties=pika.BasicProperties(
            delivery_mode=2,  # make message persistent
        )
    )

    connection.close()

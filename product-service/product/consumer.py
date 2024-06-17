# consumers.py
import json
import pika
from .rabbitmq_config import get_rabbitmq_connection, get_rabbitmq_channel
from .models import Product
import json
from decimal import Decimal


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return str(obj)
        return super(DecimalEncoder, self).default(obj)


def fetch_product_details(product_id):
    try:
        product = Product.objects.get(id=product_id)
        return {
            'id': product.id,
            'name': product.name,
            'price': product.price,
        }
    except Product.DoesNotExist:
        return None


def on_request(ch, method, props, body):
    request_data = json.loads(body)
    product_id = request_data.get('product_id')
    response = fetch_product_details(product_id)

    if response is None:
        response = {'error': 'Product not found'}

    ch.basic_publish(
        exchange='',
        routing_key='product_response_queue',
        properties=pika.BasicProperties(correlation_id=props.correlation_id),
        body=json.dumps(response, cls=DecimalEncoder)
    )
    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consuming():
    connection = get_rabbitmq_connection()
    channel = get_rabbitmq_channel(connection)

    channel.queue_declare(queue='product_request_queue', durable=True)
    channel.queue_declare(queue='product_response_queue', durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='product_request_queue', on_message_callback=on_request)

    print('Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

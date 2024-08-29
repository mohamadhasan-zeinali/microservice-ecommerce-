# rabbitmq_config.py
import pika
from config import settings


def get_rabbitmq_connection():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=settings.RABBITMQ_HOST,
        port=settings.RABBITMQ_PORT,
        credentials=pika.PlainCredentials(settings.RABBITMQ_USERNAME, settings.RABBITMQ_PASSWORD)
    ))
    return connection


def get_rabbitmq_channel(connection):
    channel = connection.channel()
    return channel

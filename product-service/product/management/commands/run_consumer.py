# run_consumer.py
from django.core.management.base import BaseCommand
from product.consumer import start_consuming


class Command(BaseCommand):
    help = 'Run the RabbitMQ consumer'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Starting RabbitMQ consumer...'))
        start_consuming()

from django.apps import AppConfig
from logpipe import register_consumer, Consumer
from .serializer import RideSerializer


class UberConfig(AppConfig):
    name = 'uber'


# Register consumers with logpipe
@register_consumer
def build_ride_consumer():

    # Run using python manage.py run_kafka_consumer
    consumer = Consumer('ride')
    consumer.register(RideSerializer)
    return consumer

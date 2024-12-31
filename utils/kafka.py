import json, time
from kafka import KafkaProducer

from core.config import settings

producer = KafkaProducer(
    bootstrap_servers=settings.KAFKA_SERVER,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def send_to_kafka(topic, obj):
    producer.send(topic, obj)

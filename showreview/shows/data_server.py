import os
import sys
import json
import pika
import django
from django.core import serializers


sys.path.append(os.path.join(sys.path[0], 'ShowsApi', 'settings.py'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ShowsApi.settings')
django.setup()

from shows.models import Review, Comment, Favorites

def handle_request(ch, method, props, body):
    username = body['username']
    _model = body['model']

    resp = {}

    if _model == 'reviews':
        queryset = Review.objects.filter(username=username)
        resp = serializers.serialize('json', queryset)
    elif _model == 'comments':
        queryset = Comment.objects.filter(username=username)
        resp = serializers.serialize('json', queryset)
    elif _model == 'favorites':
        queryset = Favorites.objects.filter(username=username)
        resp = serializers.serialize('json', queryset)
    
    ch.basic_publish(exchange='', routing_key=props.reply_to, properties=pika.BasicProperties(correlation_id = props.correlation_id),
        body=json.dumps(resp))

if __name__ == '__main__':
    params = pika.URLParameters('amqps://bwvvcnww:b4WjIHCwAtizbAo72daDwnt3IoOVgRlx@shrimp.rmq.cloudamqp.com/bwvvcnww')
    connection = pika.BlockingConnection(params)

    channel = connection.channel()
    channel.queue_declare(queue='shows_queue')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='shows_queue', on_message_callback=handle_request)

    print("Consumer is up!")

    channel.start_consuming()
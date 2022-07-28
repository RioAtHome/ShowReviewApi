import pika
import uuid
import json
import os

class RequestQueue:
    def __init__(self):
        self.params = pika.URLParameters(os.environ.get("RABBITMQ_URL"))
        self.connections = pika.BlockingConnection(self.params)

        self.channel = self.connections.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )

        self.response = None
        self.corr_id = None


    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body


    def call(self, body):
        self.response = None
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange='',
            routing_key='shows_queue',
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=json.dumps(body)
            )
        self.connections.process_data_events(time_limit=None)

        return json.loads(self.response)


import uuid

import pika


class FibClient:

    def __init__(self):
        self.connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='localhost')
        )
        self.channel = self.connection.channel()
        result = self.channel.queue_declare(queue='', exclusive=True)
        self.call_back_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.call_back_queue,
            on_message_callback=self.on_response,
        )
        self.corr_id = None
        self.response = None

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
            ch.basic_ack(delivery_tag=method.delivery_tag)

    def call(self, n):
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange='',
            routing_key='rpc_queue',
            properties=pika.BasicProperties(
                reply_to=self.call_back_queue,
                correlation_id=self.corr_id
            ),
            body=str(n),
        )
        self.connection.process_data_events(time_limit=None)
        return self.response


fib = FibClient()
response = fib.call(30)
print(response)
import pika

# We're connected now, to a broker on the local machine
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='hello_queue', durable=True)

"""
In RabbitMQ a message can never be sent directly to the queue, 
it always needs to go through an exchange.
"""

channel.basic_publish(
    exchange='',
    routing_key='hello_queue',
    body='Hello word',
    properties=pika.BasicProperties(
        delivery_mode=pika.spec.PERSISTENT_DELIVERY_MODE
))

print(" [x] Sent 'Hello World!'")

# send log message
channel.exchange_declare(exchange='logs', exchange_type='fanout')
channel.basic_publish(exchange='logs', routing_key='', body='log message')
print(" [x] Sent log message")


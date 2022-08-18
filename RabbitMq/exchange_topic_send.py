import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost')
)
channel = connection.channel()

channel.exchange_declare(exchange='topic_exchange', exchange_type='topic')

channel.basic_publish(
    exchange='topic_exchange',
    routing_key='kern.critical',
    body='A critical kernel error',
)

print(" [x] Sent message topic exchange")
connection.close()
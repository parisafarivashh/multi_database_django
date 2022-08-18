import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

result = channel.queue_declare(queue='', exclusive=True)
queue_name = result.method.queue

routing_keys = ['warning', 'info']
for routing in routing_keys:
    channel.queue_bind(
        exchange='direct_logs', queue=queue_name, routing_key=routing,
    )

print(' [*] Waiting for logs. To exit press CTRL+C')


def callback(ch, method, properties, body):
    print(f"receive message: method {method}, body:{body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(
    queue=queue_name, on_message_callback=callback)

channel.start_consuming()
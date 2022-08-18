import pika

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))
channel = connection.channel()

channel.exchange_declare(exchange='direct_logs', exchange_type='direct')

routing_keys = ['warning', 'info']
message = {'warning': 'warning message', 'info': 'info message'}
for routing in routing_keys:
    channel.basic_publish(
        exchange='direct_logs',
        routing_key=routing,
        body=message[routing],
    )

print(" [x] Sent message direct exchange")
connection.close()

import time

import pika, sys, os


def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # idempotent
    '''
    Giving a queue a name is important when you want to share 
    the queue between producers and consumers.
    '''
    channel.queue_declare(queue='hello_queue', durable=True)

    '''
     Whenever we receive a message, this callback function is called
     by the Pika library
    '''
    def callback(ch, method, properties, body):
        time.sleep(5)
        print(" [x] Received %r" % body)
        ch.basic_ack(delivery_tag=method.delivery_tag)

    '''
     we need to tell RabbitMQ that this particular callback function should
     receive messages from our hello queue:
    '''

    # prefetch_count: don't dispatch a new message to a worker until it has
    # processed and acknowledged the previous one
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue='hello_queue', on_message_callback=callback)

    # exchange logs
    channel.exchange_declare(exchange='logs', exchange_type='fanout')
    result = channel.queue_declare(queue='', exclusive=True)
    queue_name = result.method.queue
    # queue_bind: the queue is interested in messages from this exchange.
    channel.queue_bind(exchange='logs', queue=queue_name)
    channel.basic_consume(
        queue=queue_name, on_message_callback=callback)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
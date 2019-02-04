import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
channel = connection.channel()

channel.exchange_declare(
    exchange='accounts',
    exchange_type='fanout'
)

queue_name = sys.argv[1]

channel.queue_declare(queue=queue_name)

channel.queue_bind(
    exchange='accounts',
    queue=queue_name
)


def callback(ch, method, properties, body):
    print(body)


channel.basic_consume(
    callback,
    queue=queue_name,
    no_ack=True
)

channel.start_consuming()
import sys
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()

channel.exchange_declare(
    exchange='actions',
    exchange_type='topic',
)

result = channel.queue_declare(
    exclusive=True,
    durable=True,
)

queue_name = result.method.queue

for routing_key in sys.argv[1:]:
    channel.queue_bind(
        exchange='actions',
        queue=queue_name,
        routing_key=routing_key,
    )


def callback(ch, method, properties, body):
    print(body)


channel.basic_consume(
    callback,
    queue=queue_name,
)

channel.start_consuming()

'''
    python worker.py *.all
    
    python worker.py *.all *.email 
    
    python worker.py *.all *.email *.*.email *.email.*
    
    python worker.py *.all *.email *.*.email #.email.#

'''

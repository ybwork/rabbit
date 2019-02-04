import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters('127.0.0.1'))
channel = connection.channel()

channel.exchange_declare(
    exchange='actions',
    exchange_type='topic',
)

channel.basic_publish(
    exchange='actions',
    routing_key=sys.argv[1],
    body='success',
    properties=pika.BasicProperties(
        delivery_mode=2,
    )
)

print('Sent {}'.format(sys.argv[1]))

connection.close()

'''
    python task.py actions.all
    
    python task.py action.email
    
    python task.py action.sms.email
'''

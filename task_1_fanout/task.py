import pika
import sys

connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
channel = connection.channel()

channel.exchange_declare(
	exchange='accounts',
	exchange_type='fanout'
)

message = sys.argv[1]

channel.basic_publish(
	exchange='accounts',
	routing_key='',
	body=message
)

print('Sent {}'.format(message))

connection.close()
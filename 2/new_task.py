import pika
import sys

'''
	Отправляет одно сообщение в очередь
'''

# Подключаемся к брокеру на локальном хосте. Для подключения к брокеру на другой машине нужно указать её ip вместо localhost
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
channel = connection.channel()

# Создаём очередь. Если послать сообщение в несуществующую очередь, то рэбит его проигнорирует (создаёт очередь с этим именем только один раз), urable=True делает очередь устойчивой 
channel.queue_declare(queue='one', durable=True)

message = sys.argv[1]

# Отправляем сообщение в очередь
channel.basic_publish(
	exchange='',
	routing_key='hello',
	body=message,
	properties=pika.BasicProperties(
		# позволяет сделать сообщения устойчивыми
		delivery_mode = 2,
	)
)

print('sended message')

# Закрыли соединение с брокером
connection.close()
import pika
import sys

'''
	Отправляет одно сообщение в очередь
'''

# Подключаемся к брокеру на локальном хосте. Для подключения к брокеру на другой машине нужно указать её ip вместо localhost
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
channel = connection.channel()

# создаёт точку обмена
channel.exchange_declare(
	exchange='topic_logs', 
	exchange_type='topic'
)

# Создаём очередь. Если послать сообщение в несуществующую очередь, то рэбит его проигнорирует (создаёт очередь с этим именем только один раз), urable=True делает очередь устойчивой 
# channel.queue_declare(queue='one', durable=True)

# Отправляем сообщение в очередь
channel.basic_publish(
	exchange='topic_logs',
	routing_key=sys.argv[1],
	body=sys.argv[1],
	properties=pika.BasicProperties(
		# позволяет сделать сообщения устойчивыми
		delivery_mode = 2,
	)
)

print('sended message')

# Закрыли соединение с брокером
connection.close()
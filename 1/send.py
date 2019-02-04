import pika

'''
	Отправляет одно сообщение в очередь
'''

# Подключаемся к брокеру на локальном хосте. Для подключения к брокеру на другой машине нужно указать её ip вместо localhost
connection = pika.BlockingConnection(pika.ConnectionParameters(host='127.0.0.1'))
channel = connection.channel()

# Создаём очередь. Если послать сообщение в несуществующую очередь, то рэбит его проигнорирует (создаёт очередь с этим именем только один раз)
channel.queue_declare(queue='hello')

# Отправляем сообщение в очередь
channel.basic_publish(
	exchange='',
	routing_key='hello',
	body='hello world'
)

print('sended message hello world')

# Закрыли соединение с брокером
connection.close()
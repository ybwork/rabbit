import pika

# Подключаемся к брокеру на локальном хосте. Для подключения к брокеру на другой машине нужно указать её ip вместо localhost
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Создаём очередь. Если послать сообщение в несуществующую очередь, то рэбит его проигнорирует (создаёт очередь с этим именем только один раз). Создание
channel.queue_declare(queue='hello')

# При получении каждого сообщения библиотека Pika вызывает эту callback функцию (код внутри выполняет нужную работу)
def callback(ch, method, properties, body):
	message = 'Recived {}'.format(body)
	print(message)

# Обозначаем, что callback функция будет получать сообщения из очереди с именем hello
channel.basic_consume(
	callback,
	queue='hello',
	no_ack=True
)

print('[*] Waiting for messages. To exit press CTRL+C')

# Запуск бесконечного процесса, который ожидает сообщения из очереди и вызывает callback функцию
channel.start_consuming()
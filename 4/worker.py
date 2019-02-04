import pika
import time

# Подключаемся к брокеру на локальном хосте. Для подключения к брокеру на другой машине нужно указать её ip вместо localhost
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

# Создаём очередь. Если послать сообщение в несуществующую очередь, то рэбит его проигнорирует (создаёт очередь с этим именем только один раз), urable=True делает очередь устойчивой, exclusive=True позволяет создать уникальную очередь без имени 
result = channel.queue_declare(exclusive=True, durable=True)
queue_name = result.method.queue

# Связывает точку обмена с очередью
channel.queue_bind(
	exchange='direct_logs',
    queue=queue_name,
    routing_key='black' # связывает очередь с сообщениями где роут black
)

# При получении каждого сообщения библиотека Pika вызывает эту callback функцию (код внутри может быть таким, какой нам нужен)
def callback(ch, method, properties, body):
	message = 'Recived {}'.format(body)
	time.sleep(list(body).count('.'))
	print(message)
	ch.basic_ack(delivery_tag=method.delivery_tag) # отправляет поставщику сообщение о том, что задача выполнена

# подписчик не получит новое сообщение, пока не выполнит предыдущее и поставщик отправляет сообщения первому освободившемуся подписчику
channel.basic_qos(prefetch_count=1)

# Обозначаем, что callback функция будет получать сообщения из очереди с именем hello
channel.basic_consume(
	callback,
	queue=queue_name,
)

print('Waiting for messages. To exit press CTRL+C')

# Запуск бесконечного процесса, который ожидает сообщения из очереди и вызывает callback функцию
channel.start_consuming()
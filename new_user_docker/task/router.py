import pika

credentials = pika.PlainCredentials('yet', 'asdfasdf')

parameters = pika.ConnectionParameters(
    '172.17.0.1',
    port=5672,
    credentials=credentials
)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

exchange_name = 'router'

channel.exchange_declare(
    exchange=exchange_name,
    exchange_type='direct'
)

result = channel.queue_declare(
    exclusive=True,
    durable=True
)

queue_name = result.method.queue

channel.queue_bind(
    exchange=exchange_name,
    queue=queue_name,
    routing_key=exchange_name
)

def send_event(exchange_name):
    channel.exchange_declare(
        exchange=exchange_name,
        exchange_type='direct'
    )

    channel.basic_publish(
        exchange=exchange_name,
        routing_key=exchange_name,
        body=exchange_name,
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )

def callback(channel, method, properties, body):
    event = body.decode('utf-8')

    if event == 'create_user':
        send_event(exchange_name='add_user_to_mail')
    elif event == 'add_user_to_redmine':
        send_event(exchange_name='add_user_to_redmine')

channel.basic_consume(
    callback,
    queue=queue_name
)

channel.start_consuming()

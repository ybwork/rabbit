import pika

credentials = pika.PlainCredentials('yet', 'asdfasdf')

parameters = pika.ConnectionParameters(
    '172.17.0.1',
    port=5672,
    credentials=credentials
)

connection = pika.BlockingConnection(parameters)

channel = connection.channel()

exchange_name = 'add_user_to_mail'

channel.exchange_declare(
    exchange=exchange_name,
    exchange_type='direct',
)

channel.queue_declare(
    queue=exchange_name,
    durable=True,
)

channel.queue_bind(
    exchange=exchange_name,
    queue=exchange_name,
    routing_key=exchange_name,
)


def callback(ch, method, properties, body):
    print('User added to email')

    exchange_name = 'router'

    channel.exchange_declare(
        exchange=exchange_name,
        exchange_type='direct'
    )

    channel.basic_publish(
        exchange=exchange_name,
        routing_key=exchange_name,
        body='add_user_to_redmine',
        properties=pika.BasicProperties(
            delivery_mode=2
        )
    )


channel.basic_consume(
    callback,
    queue=exchange_name,
)

channel.start_consuming()

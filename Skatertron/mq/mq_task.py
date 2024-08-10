import pika


class MQTask:

    @staticmethod
    def new_task(mq_connection, message="Test!", queue='task_queue'):
        channel = mq_connection.channel()

        channel.queue_declare(queue=queue, durable=True)

        message_body = message
        channel.basic_publish(
            exchange='',
            routing_key='task_queue',
            body=message_body,
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent
            ))
        print(f" [x] Sent {message_body}")

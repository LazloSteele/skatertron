import pika
import sys


class MQTask:

    @staticmethod
    def new_task(message = "Test!"):
        with pika.BlockingConnection(pika.ConnectionParameters(host='localhost')) as connection:
            channel = connection.channel()

            channel.queue_declare(queue='task_queue', durable=True)

            message_body = message
            channel.basic_publish(
                exchange='',
                routing_key='task_queue',
                body=message_body,
                properties=pika.BasicProperties(
                    delivery_mode=pika.DeliveryMode.Persistent
                ))
            print(f" [x] Sent {message_body}")
            connection.close()


if __name__ == "__main__":
    MQTask.new_task(' '.join(sys.argv[1:]))
import pika
import time


class MQWorker:
    def __init__(self, connection):
        self.connection = connection
        self.channel = self.connection.channel()

        self.channel.queue_declare(queue='task_queue', durable=True)
        print(' [*] Waiting for messages. To exit press CTRL+C')

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue='task_queue', on_message_callback=self.callback)

        self.channel.start_consuming()

    @staticmethod
    def callback(self, ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)


if __name__ == "__main__":
    with pika.BlockingConnection(pika.ConnectionParameters(host='localhost')) as connection:
        worker = MQWorker(connection)


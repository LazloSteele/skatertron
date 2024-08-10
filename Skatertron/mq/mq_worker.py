import pika
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


class MQWorker:
    def __init__(self, host='localhost', queue='task_queue'):
        self.connection = None
        self.channel = None
        self.host = host
        self.queue = queue

        self.connect()

    def connect(self):
        try:
            self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
            self.channel = self.connection.channel()
            self.channel.queue_declare(queue=self.queue)

            logging.info('Connected to RabbitMQ')
            print(' [*] Waiting for messages. To exit press CTRL+C')

            self.channel.basic_qos(prefetch_count=1)
            self.channel.basic_consume(queue='task_queue', on_message_callback=self.callback)

            self.channel.start_consuming()
        except Exception as e:
            logging.error(f'Failed to connect to RabbitMQ: {e}')

    def close_connection(self):
        if self.connection and self.connection.is_open:
            self.connection.close()
            logging.info('RabbitMQ connection closed')
            print('[*] Connection closed. Goodnight!')

    @staticmethod
    def callback(self, ch, method, properties, body):
        print(f" [x] Received {body.decode()}")
        time.sleep(body.count(b'.'))
        print(" [x] Done")
        ch.basic_ack(delivery_tag=method.delivery_tag)

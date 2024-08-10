import pika


class MQSend:

    @staticmethod
    def send(message_body: bytes):
        with pika.BlockingConnection(pika.ConnectionParameters('localhost')) as connection:
            channel = connection.channel()

            channel.queue_declare(queue='mq_messages')

            channel.basic_publish(exchange='',
                                  routing_key='mq_messages',
                                  body=message_body)

            print(f" [x] Sent '{message_body}'")

            connection.close()

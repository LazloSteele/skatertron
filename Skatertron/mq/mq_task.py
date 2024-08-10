import sys


message_body = ' '.join(sys.argv[1:]) or "Test Message!"
channel.basic_publish(exchange='',
                      routing_key='mq_messages',
                      body=message_body)
print(f" [x] Sent {message_body}")

# spark_demo/S_ML/base/rabbitmq_consumer.py
import pika
import os
from dotenv import load_dotenv
import time

class RabbitMQConsumer:
    def __init__(self):
        load_dotenv()
        self.connection = self.create_connection()
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue='task_queue', durable=True)

    def create_connection(self):
        attempts = 5
        for i in range(attempts):
            try:
                return pika.BlockingConnection(
                    pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST')))
            except pika.exceptions.AMQPConnectionError as e:
                print(f"連接失敗，重試 ({i+1}/{attempts})...")
                time.sleep(5)
        raise Exception("無法連接到 RabbitMQ 服務")

    def start_consuming(self):
        self.channel.basic_consume(queue='task_queue', on_message_callback=self.callback, auto_ack=True)
        print('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()

    def callback(self, ch, method, properties, body):
        print(f"Received {body}")
        # 在這裡處理消息

    def stop(self):
        self.connection.close()

if __name__ == '__main__':
    consumer = RabbitMQConsumer()
    consumer.start_consuming()

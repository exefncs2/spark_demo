# -*- coding: utf-8 -*-
# pylint: disable=C0111,C0103,R0205

import functools
import logging
import threading
import time
import pika
from pika.exchange_type import ExchangeType
from dotenv import load_dotenv
import os

class RabbitMQConsumerEngine:
    def __init__(self, exchange, exchange_type, queue, routing_key, heartbeat=10, prefetch_count=1):
        load_dotenv()
        
        self.LOG_FORMAT = ('%(levelname) -10s %(asctime)s %(name) -30s %(funcName) '
                           '-35s %(lineno) -5d: %(message)s')
        logging.basicConfig(level=logging.DEBUG, format=self.LOG_FORMAT)
        self.LOGGER = logging.getLogger(__name__)

        self.credentials = pika.PlainCredentials(os.getenv("RABBITMQ_USER"), os.getenv("RABBITMQ_PASSWORD"))
        self.parameters = pika.ConnectionParameters(
            'localhost', credentials=self.credentials, heartbeat=heartbeat)
        self.connection = pika.BlockingConnection(self.parameters)
        self.channel = self.connection.channel()

        self.exchange = exchange
        self.exchange_type = exchange_type
        self.queue = queue
        self.routing_key = routing_key
        self.prefetch_count = prefetch_count
        self.threads = []

        self.setup()

    def setup(self):
        self.channel.exchange_declare(
            exchange=self.exchange,
            exchange_type=self.exchange_type,
            passive=False,
            durable=True,
            auto_delete=False)
        self.channel.queue_declare(queue=self.queue, auto_delete=True)
        self.channel.queue_bind(
            queue=self.queue, exchange=self.exchange, routing_key=self.routing_key)
        self.channel.basic_qos(prefetch_count=self.prefetch_count)

    def ack_message(self, ch, delivery_tag):
        if ch.is_open:
            ch.basic_ack(delivery_tag)
        else:
            pass

    def do_work(self, ch, delivery_tag, body):
        thread_id = threading.get_ident()
        self.LOGGER.info('Thread id: %s Delivery tag: %s Message body: %s', thread_id,
                    delivery_tag, body)
        time.sleep(10)
        cb = functools.partial(self.ack_message, ch, delivery_tag)
        ch.connection.add_callback_threadsafe(cb)

    def on_message(self, ch, method_frame, _header_frame, body):
        delivery_tag = method_frame.delivery_tag
        t = threading.Thread(target=self.do_work, args=(ch, delivery_tag, body))
        t.start()
        self.threads.append(t)

    def start_consuming(self):
        on_message_callback = functools.partial(self.on_message)
        self.channel.basic_consume(on_message_callback=on_message_callback, queue=self.queue)
        try:
            self.channel.start_consuming()
        except KeyboardInterrupt:
            self.channel.stop_consuming()

        for thread in self.threads:
            thread.join()

        self.connection.close()

if __name__ == "__main__":
    engine = RabbitMQConsumerEngine(
        exchange="test_exchange",
        exchange_type=ExchangeType.direct,
        queue="standard",
        routing_key="standard_key"
    )
    engine.start_consuming()

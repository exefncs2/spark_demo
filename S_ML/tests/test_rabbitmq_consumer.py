# spark_demo/S_ML/tests/test_rabbitmq_consumer.py
import pytest
import pika
from base.rabbitmq_consumer import RabbitMQConsumer

@pytest.fixture
def mock_rabbitmq(mocker):
    # 模擬 BlockingConnection
    mock_connection = mocker.patch('pika.BlockingConnection')
    # 模擬 channel 方法
    mock_channel = mocker.Mock()
    mock_connection.return_value.channel.return_value = mock_channel
    return mock_channel

def test_start_consuming(mock_rabbitmq):
    consumer = RabbitMQConsumer()
    consumer.start_consuming()
    mock_rabbitmq.basic_consume.assert_called_once_with(queue='task_queue', on_message_callback=consumer.callback, auto_ack=True)
    mock_rabbitmq.start_consuming.assert_called_once()

def test_callback(mocker, mock_rabbitmq):
    consumer = RabbitMQConsumer()
    mock_print = mocker.patch('builtins.print')
    body = "test message"
    consumer.callback(None, None, None, body)
    mock_print.assert_called_with(f"Received {body}")

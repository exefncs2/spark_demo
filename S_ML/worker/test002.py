import os
import json
import queue
import threading
import time
import pandas as pd
from base.rabbitmq_consumer import RabbitMQConsumerEngine
from base.spark_engine import SparkEngine
from base.psql_connector import PsqlConnector
from model.wine_quality_predictions_model import WineQualityPrediction
from dotenv import load_dotenv
import logging

load_dotenv()

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 创建线程安全的队列
local_queue = queue.Queue()

def callback(body):
    logger.info("Received message:")
    message = json.loads(body)
    logger.info(message)
    local_queue.put(message)

def process_messages():
    # 使用 Spark 处理数据
    spark_engine = SparkEngine("WineQualityPrediction")

    # 从本地队列中读取所有消息
    messages = []
    while not local_queue.empty():
        messages.append(local_queue.get())
    print(f"messages: {messages}")
    
    if messages:
        processed_data = spark_engine.process_data(messages)

        if processed_data is not None:
            # 将处理后的数据转换为 Pandas DataFrame
            pandas_df = processed_data.toPandas()

            # 使用 PsqlConnector 将数据写入 PostgreSQL
            psql_connector = PsqlConnector()
            table_name = "wine_quality_predictions"

            # 创建表结构
            create_table_query = f'''
            CREATE TABLE IF NOT EXISTS "DWH".{table_name} (
                id SERIAL PRIMARY KEY,
                prediction FLOAT,
                residual_sugar FLOAT
            )
            '''
            psql_connector.execute_command(create_table_query)

            # 将数据写入 PostgreSQL
            try:
                for index, row in pandas_df.iterrows():
                    # 使用 Pydantic 模型来进行数据验证和转换
                    prediction_data = WineQualityPrediction(
                        id=index,
                        prediction=row['prediction'],
                        residual_sugar=row['residual_sugar']
                    )
                    insert_query = f'''
                    INSERT INTO "DWH".{table_name} (id, prediction, residual_sugar)
                    VALUES ({prediction_data.id},{prediction_data.prediction}, {prediction_data.residual_sugar})
                    '''
                    psql_connector.execute_command(insert_query)
                    print(f"輸出 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<DWH.{table_name}<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                    
                logger.info(f"Data written to PostgreSQL table {table_name}")
            except Exception as e:
                logger.error(f"Error writing data to PostgreSQL: {e}")
                logger.error(f"Exception details: {e.__class__.__name__}: {str(e)}")

    spark_engine.stop()

def consume_predictions():
    exchange = "wine_quality_exchange"
    queue = "wine_quality_predictions"
    routing_key = "wine_quality"

    rabbitmq_engine = RabbitMQConsumerEngine(
        exchange=exchange,
        exchange_type='direct',
        queue=queue,
        routing_key=routing_key,
        callback=callback,
        durable=True,
        auto_delete=False
    )

    logger.info('Waiting for messages. To exit press CTRL+C')
    rabbitmq_engine.start_consuming()

if __name__ == "__main__":
    # 启动RabbitMQ消费者
    consumer_thread = threading.Thread(target=consume_predictions)
    consumer_thread.start()

    # 定期处理本地队列中的消息
    while True:
        process_messages()
        time.sleep(60)  # 每60秒处理一次消息

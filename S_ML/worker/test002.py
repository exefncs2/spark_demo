import os
import orjson as json
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
import uuid

load_dotenv()

# 設置日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 創建線程安全的隊列
local_queue = queue.Queue()

def callback(body):
    logger.info("收到消息:")
    message = json.loads(body)
    logger.info(message)
    local_queue.put(message)

def process_messages():
    # 使用 Spark 處理數據
    spark_engine = SparkEngine("WineQualityPrediction")

    # 從本地隊列中讀取所有消息
    messages = []
    while not local_queue.empty():
        messages.append(local_queue.get())
    logger.info(f"messages: {messages}")
    
    if messages:
        processed_data = spark_engine.process_data(messages)

        if processed_data is not None:
            # 將處理後的數據轉換為 Pandas DataFrame
            pandas_df = processed_data.toPandas()

            # 使用 PsqlConnector 將數據寫入 PostgreSQL
            psql_connector = PsqlConnector()
            table_name = "wine_quality_predictions"

            # 創建表結構
            create_table_query = f'''
            CREATE TABLE IF NOT EXISTS "DWH".{table_name} (
                id uuid PRIMARY KEY,
                prediction FLOAT,
                residual_sugar FLOAT
            )
            '''
            psql_connector.execute_command(create_table_query)

            # 將數據寫入 PostgreSQL
            try:
                for index, row in pandas_df.iterrows():
                    # 使用 Pydantic 模型來進行數據驗證和轉換
                    prediction_data = WineQualityPrediction(
                        id=f"'{str(uuid.uuid4())}'",
                        prediction=row['prediction'],
                        residual_sugar=row['residual_sugar']
                    )
                    insert_query = f'''
                    INSERT INTO "DWH".{table_name} (id, prediction, residual_sugar)
                    VALUES ({prediction_data.id},{prediction_data.prediction}, {prediction_data.residual_sugar})
                    '''
                    psql_connector.execute_command(insert_query)
                    logger.info(f"輸出 <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<DWH.{table_name}<<<<<<<<<<<<<<<<<<<<<<<<<<<")
                    
                logger.info(f"數據寫入 PostgreSQL 表 {table_name}")
            except Exception as e:
                logger.error(f"寫入數據到 PostgreSQL 時出錯: {e}")
                logger.error(f"異常詳情: {e.__class__.__name__}: {str(e)}")

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

    logger.info('等待消息中。按下 CTRL+C 退出')
    rabbitmq_engine.start_consuming()

def monitor_and_process():
    while True:
        if not local_queue.empty():
            process_messages()
        time.sleep(1)  # 每秒檢查一次隊列是否有消息

if __name__ == "__main__":
    # 啟動 RabbitMQ 消費者
    consumer_thread = threading.Thread(target=consume_predictions)
    consumer_thread.start()

    # 監聽並處理本地隊列中的消息
    monitor_and_process()

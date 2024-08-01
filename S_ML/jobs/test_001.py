# jobs/test_001.py
import logging
from center.psql_to_redis import load_table_to_redis
from center.redis_ml_to_rabbitmq import read_data_from_redis, process_data_with_spark, send_predictions_to_rabbitmq

# 設置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    # 定義參數
    Schema = "ODS"
    tables = ['wine_quality_red', 'wine_quality_white']
    redis_key_prefix = 'wine_quality'

    # 將數據從 PostgreSQL 加載到 Redis
    for table in tables:
        load_table_to_redis(Schema, table, redis_key_prefix)

    # 從 Redis 中讀取數據
    redis_key = f"{redis_key_prefix}:wine_quality_red"
    data = read_data_from_redis(redis_key)

    if data is not None:
        # 使用 PySpark 處理數據並進行預測
        predictions = process_data_with_spark(data)

        # 將預測結果發送到 RabbitMQ
        send_predictions_to_rabbitmq(predictions)

if __name__ == "__main__":
    main()

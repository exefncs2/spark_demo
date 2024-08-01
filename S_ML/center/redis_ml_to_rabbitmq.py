import os
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import DecisionTreeRegressor
from pyspark.ml.evaluation import RegressionEvaluator
from base.redis_engine import RedisEngine
from base.psql_connector import PsqlConnector
from base.rabbitmq_consumer import RabbitMQConsumerEngine
from base.spark_engine import SparkEngine
from dotenv import load_dotenv
import orjson
import logging

load_dotenv()


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_data_from_redis(redis_key):
    redis_engine = RedisEngine()
    data_json = redis_engine.get_value(redis_key)
    if data_json:
        data = pd.read_json(data_json, orient='split')
        return data
    else:
        logger.error(f"No data found for key: {redis_key}")
        return None

def process_data_with_spark(data):
    # 初始化SparkSession
    spark_engine = SparkEngine("WineQualityPrediction")
    spark = spark_engine.spark

    # 將Pandas DataFrame轉換為Spark DataFrame
    df = spark.createDataFrame(data)

    # 特徵選擇
    feature_columns = data.columns.tolist()
    feature_columns.remove('residual_sugar')  # 假設 'residual_sugar' 是我們要預測的列
    assembler = VectorAssembler(inputCols=feature_columns, outputCol="features")
    df = assembler.transform(df)

    # 分割數據集
    train_data, test_data = df.randomSplit([0.8, 0.2], seed=1234)

    # 構建決策樹模型
    dt = DecisionTreeRegressor(labelCol="residual_sugar", featuresCol="features")
    model = dt.fit(train_data)

    # 預測
    predictions = model.transform(test_data)

    # 評估模型
    evaluator = RegressionEvaluator(labelCol="residual_sugar", predictionCol="prediction", metricName="rmse")
    rmse = evaluator.evaluate(predictions)
    logger.info(f"Root Mean Squared Error (RMSE) on test data = {rmse}")

    # 返回預測結果
    return predictions.select("prediction", "residual_sugar").toPandas()

def send_predictions_to_rabbitmq(predictions,durable=True, auto_delete=False):
    # 設置 RabbitMQ 連接
    exchange = "wine_quality_exchange"
    queue = "wine_quality_predictions"
    routing_key = "wine_quality"

    rabbitmq_engine = RabbitMQConsumerEngine(
        exchange=exchange,
        exchange_type='direct',
        queue=queue,
        callback="test",
        routing_key=routing_key,
        durable=durable,
        auto_delete=auto_delete
    )

    # 發送預測結果
    for index, row in predictions.iterrows():
        message = orjson.dumps(row.to_dict())
        rabbitmq_engine.channel.basic_publish(exchange=exchange, routing_key=routing_key, body=message)
        logger.info(f"Sent prediction to RabbitMQ: {message}")

    # 關閉連接
    rabbitmq_engine.connection.close()

if __name__ == "__main__":
    # 從 Redis 中讀取數據
    redis_key = "wine_quality:wine_quality_red"
    data = read_data_from_redis(redis_key)

    if data is not None:
        # 使用 PySpark 處理數據並進行預測
        predictions = process_data_with_spark(data)

        # 將預測結果發送到 RabbitMQ
        send_predictions_to_rabbitmq(predictions)

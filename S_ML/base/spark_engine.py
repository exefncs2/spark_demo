# spark_demo/S_ML/base/spark_engine.py
from pyspark.sql import SparkSession
import os
from dotenv import load_dotenv

class SparkEngine:
    def __init__(self, app_name):
        load_dotenv()
        self.spark = SparkSession.builder \
            .appName(app_name) \
            .master(os.getenv('SPARK_MASTER_URL')) \
            .getOrCreate()

    def run_job(self, data, columns):
        df = self.spark.createDataFrame(data, columns)
        df.show()

    def stop(self):
        self.spark.stop()

if __name__ == '__main__':
    engine = SparkEngine("test")
    sample_data = [("Alice", 34), ("Bob", 45), ("Cathy", 29)]
    columns = ["Name", "Age"]
    engine.run_job(sample_data, columns)
    engine.stop()

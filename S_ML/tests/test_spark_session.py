# spark_demo/S_ML/base/test_spark_engine.py
import pytest
from pyspark.sql import SparkSession
from base.spark_engine import SparkEngine

class TestSparkEngine:
    @pytest.fixture(scope="class")
    def spark_engine(self):
        engine = SparkEngine()
        yield engine
        engine.stop()

    def test_spark_session(self, spark_engine):
        assert isinstance(spark_engine.spark, SparkSession)

    def test_run_job(self, spark_engine):
        sample_data = [("Alice", 34), ("Bob", 45), ("Cathy", 29)]
        columns = ["Name", "Age"]
        spark_engine.run_job(sample_data, columns)

        df = spark_engine.spark.createDataFrame(sample_data, columns)
        collected_data = df.collect()
        assert len(collected_data) == 3
        assert collected_data[0]["Name"] == "Alice"
        assert collected_data[1]["Age"] == 45

    def test_stop(self, spark_engine):
        spark_engine.stop()
        assert not spark_engine.spark._jsparkSession.isStopped()

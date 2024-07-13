import pytest
from base import SparkBaseEngine

def test_spark_connection():
    engine = SparkBaseEngine()
    spark = engine.get_spark_session()
    assert spark is not None
    assert "version" in dir(spark)
    print("Spark Version:", spark.version)
    engine.stop_spark_session()

if __name__ == "__main__":
    pytest.main([__file__])

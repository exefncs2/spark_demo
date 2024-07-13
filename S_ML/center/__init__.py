from base import SparkBaseEngine

def get_spark_session(app_name="S_ML_App", master="local[*]"):
    engine = SparkBaseEngine(app_name, master)
    return engine.get_spark_session()

# 測試 get_spark_session
if __name__ == "__main__":
    spark = get_spark_session()
    print("Spark Version:", spark.version)
    spark.stop()
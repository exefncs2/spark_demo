from pyspark.sql import SparkSession

class SparkBaseEngine:
    def __init__(self, app_name="S_ML_App", master="local[*]"):
        """
        初始化 Spark Session
        :param app_name: Spark 應用名稱
        :param master: Spark Master 節點，默認為本地模式
        """
        self.app_name = app_name
        self.master = master
        self.spark = None
        self._create_spark_session()

    def _create_spark_session(self):
        """
        創建 Spark Session
        """
        self.spark = SparkSession.builder \
            .appName(self.app_name) \
            .master(self.master) \
            .getOrCreate()
        print(f"Spark Session created with app name {self.app_name} and master {self.master}")

    def get_spark_session(self):
        """
        獲取 Spark Session
        :return: SparkSession
        """
        return self.spark

    def stop_spark_session(self):
        """
        停止 Spark Session
        """
        if self.spark:
            self.spark.stop()
            print("Spark Session stopped")

# 測試 SparkBaseEngine
if __name__ == "__main__":
    engine = SparkBaseEngine()
    spark = engine.get_spark_session()
    # 測試代碼，例如顯示 Spark 版本
    print("Spark Version:", spark.version)
    engine.stop_spark_session()
# S_ML
這是一個demo只展示方法
測試前置要求spark RABBITMQ PSQL redis已配置好的環境並用.env 設定連線
安裝好基本環境後
在PSQL上建立ODS（Operational Data Store）、DWH（Data Warehouse）和 DM（Data Mart）三個Schema
   ODS（Operational Data Store）：存放操作數據，支持當前操作需求，數據詳細且臨時。
   DWH（Data Warehouse）：存放整合的歷史數據，支持戰略決策和數據分析。
   DM（Data Mart）：針對特定業務部門或功能的子集數據存儲，從數據倉庫中提取數據並進行優化。
notebooks有insert_test_data.ipynb 可以直接灌測試資料
資料來源
   https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-red.csv
   https://archive.ics.uci.edu/ml/machine-learning-databases/wine-quality/winequality-white.csv
已有一個jobs(test_001.py)可以將資料丟到redis並丟到rabbitMQ儲列[wine_quality_predictions](有些版本要先手動建立)跟一個worker可以監聽exchange[wine_quality_exchange]

!此測試設置id因此會有沒清空無法正常寫入的現象



## Structure
基礎:
   base/: 包含基礎引擎和核心功能。
巨集:
   center/: 處理重複功能例如:特定(固定)的處理方式，或是可能多次重複的功能。
工具:
   model/: 輸出入模型。
   tests/: pytest。
   util/: 包含實用工具函數。
工作類型:
   jobs/: 一次性(定時)作業。
   worker/: 包含持續工作的作業，如監聽 RabbitMQ 或等待檔案進入等等。

## Setup

Install the required packages:

   pip install -r requirements.txt


## future
1. 引入 prefect 或 airflow 排程管理工具 後台管理pyspark 又或者引入k8s後臺管理
2. 更多樣的測試
3. 完整的文件
4. 完善pytest
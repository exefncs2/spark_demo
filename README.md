# S_ML

This is a Spark Machine Learning project.

## Structure

base/: 包含基礎引擎和核心功能。
center/: 處理 Spark 通訊和連接。
jobs/: 定時作業。
model/: 輸出入模型。
tests/: pytest。
util/: 包含實用工具函數。
worker/: 包含持續工作的作業，如監聽 RabbitMQ 或等待檔案進入等等。

## Setup

1. Install the required packages:

   pip install -r requirements.txt


# S_ML
這是一個 demo，旨在展示方法。

## 測試前置要求

確保 Spark、RabbitMQ、PostgreSQL 和 Redis 已配置好環境，並使用 `.env` 文件設定連線。

### 安裝基本環境後

在 PostgreSQL 上建立 ODS（Operational Data Store）、DWH（Data Warehouse）和 DM（Data Mart）三個 Schema：

- **ODS（Operational Data Store）**：存放操作數據，支持當前操作需求，數據詳細且臨時。
- **DWH（Data Warehouse）**：存放整合的歷史數據，支持戰略決策和數據分析。
- **DM（Data Mart）**：針對特定業務部門或功能的子集數據存儲，從數據倉庫中提取數據並進行優化。

### 插入測試資料

在 `notebooks` 目錄下有 `insert_test_data.ipynb`，可以直接用來灌測試資料。

資料來源：
- [紅酒數據](https:archive.ics.uci.edumlmachine-learning-databaseswine-qualitywinequality-red.csv)
- [白酒數據](https:archive.ics.uci.edumlmachine-learning-databaseswine-qualitywinequality-white.csv)

### 現有的 Jobs 和 Worker

已經有一個 jobs（`test_001.py`），可以將資料丟到 Redis 並發送到 RabbitMQ 隊列 `[wine_quality_predictions]`（有些版本需要先手動建立）。還有一個 worker 可以監聽 exchange `[wine_quality_exchange]`。

> 注意：此測試設置 ID，因此會有因為未清空而無法正常寫入的情況發生。

## Structure

### 基礎
- `base`：包含基礎引擎和核心功能。

### 巨集
- `center`：處理重複功能，例如特定（固定）的處理方式或多次重複的功能。

### 工具
- `model`：輸出入模型。
- `tests`：pytest 測試。
- `util`：包含實用工具函數。

### 工作類型
- `jobs`：一次性（定時）作業。
- `worker`：包含持續工作的作業，如監聽 RabbitMQ 或等待檔案進入等。

## Setup

安裝所需的套件：

```bash
pip install -r requirements.txt
```

## Future

1. 引入 Prefect 或 Airflow 排程管理工具，後台管理 PySpark，或引入 Kubernetes 後台管理。
2. 增加更多樣的測試。
3. 完整的文件。
4. 完善 pytest 測試。

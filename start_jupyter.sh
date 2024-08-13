#!/bin/bash

# 啟動虛擬環境
source venv/bin/activate

# 配置 PySpark 環境變量
export SPARK_HOME=$(dirname $(dirname $(readlink -f $(which pyspark))))
export PYTHONPATH=$SPARK_HOME/python/:$SPARK_HOME/python/lib/py4j-0.10.9.5-src.zip:$PYTHONPATH
export PYSPARK_PYTHON=python3
export PYSPARK_DRIVER_PYTHON=python3

# 啟動 Jupyter Notebook
jupyter notebook


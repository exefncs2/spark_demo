# center/psql_to_redis.py
import pandas as pd
from base.psql_connector import PsqlConnector
from base.redis_engine import RedisEngine

def load_table_to_redis(schma_name,table_name, redis_key_prefix):
    """
    從PostgreSQL讀取數據，轉換格式並存儲到Redis

    :param schma_name 從PostgreSQL讀取的schma
    :param table_name: 從PostgreSQL讀取的表名
    :param redis_key_prefix: 存儲到Redis中的鍵名前綴
    """
    # 使用 PsqlConnector 從 PostgreSQL 中讀取數據
    psql_connector = PsqlConnector()
    query = f'SELECT * FROM "{schma_name}".{table_name}'
    data = psql_connector.execute_query(query)

    # 將數據轉換為 DataFrame
    df = pd.DataFrame(data)

    # 轉換數據格式
    data_json = df.to_json(orient='split')

    # 使用 RedisEngine 將數據存儲到 Redis
    redis_engine = RedisEngine()
    redis_key = f'{redis_key_prefix}:{table_name}'
    redis_engine.set_value(redis_key, data_json)

    print(f"Data from {table_name} loaded into Redis with key: {redis_key}")

if __name__ == "__main__":
    # 指定要加載的表名和 Redis 鍵名前綴
    schma = "ODS"
    tables = ['wine_quality_red', 'wine_quality_white']
    redis_key_prefix = 'wine_quality'

    for table in tables:
        load_table_to_redis(schma,table, redis_key_prefix)

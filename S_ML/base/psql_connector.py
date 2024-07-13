# spark_demo/S_ML/base/psql_connector.py
from dotenv import load_dotenv
import os
import psycopg2
from pydantic import BaseModel

class PsqlConnector:
    def __init__(self):
        load_dotenv()
        self.connection = psycopg2.connect(
            host=os.getenv('PG_HOST'),
            port=os.getenv('PG_PORT'),
            dbname=os.getenv('PG_DB')
            # 使用 Kerberos 或其他方式认证，不使用用户名和密码
        )

    def query(self, sql_query, params=None):
        cursor = self.connection.cursor()
        cursor.execute(sql_query, params)
        columns = [desc[0] for desc in cursor.description]
        result = cursor.fetchall()
        cursor.close()
        return [dict(zip(columns, row)) for row in result]

    def insert(self, sql_insert, data: BaseModel):
        cursor = self.connection.cursor()
        cursor.execute(sql_insert, data.dict().values())
        self.connection.commit()
        cursor.close()

    def update(self, sql_update, data: BaseModel):
        cursor = self.connection.cursor()
        cursor.execute(sql_update, data.dict().values())
        self.connection.commit()
        cursor.close()

    def delete(self, sql_delete, params):
        cursor = self.connection.cursor()
        cursor.execute(sql_delete, params)
        self.connection.commit()
        cursor.close()

    def close(self):
        self.connection.close()

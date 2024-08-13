# spark_demo/S_ML/base/psql_connector.py
from dotenv import load_dotenv
import os
import psycopg2

class PsqlConnector:
    def __init__(self):
        load_dotenv()
        self.connection = psycopg2.connect(
            host=os.getenv('PG_HOST'),
            port=os.getenv('PG_PORT'),
            dbname=os.getenv('PG_DB'),
            user=os.getenv('PG_USER'),
            password=os.getenv('PG_PASSWORD'),
        )

    def execute_query(self, sql_query):
        cursor = self.connection.cursor()
        cursor.execute(sql_query)
        columns = [desc[0] for desc in cursor.description]
        result = cursor.fetchall()
        cursor.close()
        return [dict(zip(columns, row)) for row in result]

    def execute_command(self, sql_command):
        cursor = self.connection.cursor()
        cursor.execute(sql_command)
        self.connection.commit()
        cursor.close()

    def close_connection(self):
        self.connection.close()

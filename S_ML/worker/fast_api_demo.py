from fastapi import FastAPI
from base.psql_connector import PsqlConnector
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
app = FastAPI()
app.mount("/static", StaticFiles(directory="S_ML/interface"), name="static")

@app.get("/")
def read_root():
    return FileResponse("S_ML/interface/vue3_demo.html")

@app.get("/predictions/")
def get_predictions():
    # 实例化 PsqlConnector
    connector = PsqlConnector()
    
    # 执行查询
    query = 'SELECT * FROM "DWH".wine_quality_predictions'
    results = connector.execute_query(query)
    
    # 关闭数据库连接
    connector.close_connection()
    
    return results

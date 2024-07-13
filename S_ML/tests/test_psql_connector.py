# spark_demo/S_ML/tests/test_psql_connector.py
import pytest
from S_ML.base.psql_connector import PsqlConnector

@pytest.fixture
def psql_connector():
    connector = PsqlConnector()
    yield connector
    connector.close()

def test_query(psql_connector):
    # 測試查詢一個已知的表
    result = psql_connector.query("SELECT 1")
    assert result == [(1,)], "應該返回[(1,)]"

def test_invalid_query(psql_connector):
    # 測試無效的查詢
    with pytest.raises(Exception):
        psql_connector.query("SELECT * FROM non_existent_table")

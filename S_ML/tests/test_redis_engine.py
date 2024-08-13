import pytest
import time
from base.redis_engine import redis_engine

@pytest.fixture(scope="module")
def redis_client():
    """Fixture to provide a Redis client."""
    return redis_engine.client

def test_set_and_get_value(redis_client):
    """Test setting and getting a value."""
    redis_client.set('test_key', 'test_value')
    value = redis_client.get('test_key')
    assert value == 'test_value', f"Expected 'test_value' but got {value}"
    redis_client.delete('test_key')  # 清理

def test_set_value_with_ttl(redis_client):
    """Test setting a value with TTL."""
    redis_client.setex('test_key', 1, 'test_value')  # 設置 TTL 為 1 秒
    time.sleep(2)  # 等待 2 秒
    value = redis_client.get('test_key')
    assert value is None, f"Expected None but got {value}"

def test_hset_and_hget(redis_client):
    """Test setting and getting a hash value."""
    redis_client.hset('test_hash', 'field1', 'value1')
    value = redis_client.hget('test_hash', 'field1')
    assert value == 'value1', f"Expected 'value1' but got {value}"
    redis_client.delete('test_hash')  # 清理

def test_hdel(redis_client):
    """Test deleting a hash value."""
    redis_client.hset('test_hash', 'field1', 'value1')
    redis_client.hdel('test_hash', 'field1')
    value = redis_client.hget('test_hash', 'field1')
    assert value is None, f"Expected None but got {value}"

def test_exists(redis_client):
    """Test checking if a key exists."""
    redis_client.set('test_key', 'test_value')
    exists = redis_client.exists('test_key')
    assert exists == 1, f"Expected key to exist, but it does not"
    redis_client.delete('test_key')  # 清理

def test_delete_value(redis_client):
    """Test deleting a value."""
    redis_client.set('test_key', 'test_value')
    redis_client.delete('test_key')
    value = redis_client.get('test_key')
    assert value is None, f"Expected None but got {value}"

import redis
from dotenv import load_dotenv
import os

# 加載 .env 文件中的配置
load_dotenv()

class RedisEngine:
    def __init__(self, host='localhost', port=6379, password=None):
        """
        初始化 Redis 客戶端。

        :param host: Redis 伺服器的主機名或 IP 地址，默認為 'localhost'
        :param port: Redis 伺服器的端口號，默認為 6379
        :param password: Redis 伺服器的密碼，默認為 None
        """
        self.host = host
        self.port = port
        self.password = password
        self.client = None
        self.connect()

    def connect(self):
        """連接到 Redis 伺服器。"""
        try:
            self.client = redis.StrictRedis(
                host=self.host,
                port=self.port,
                password=self.password,
                decode_responses=True
            )
            # 測試連接
            self.client.ping()
            print("Successfully connected to Redis")
        except redis.ConnectionError as e:
            print(f"Failed to connect to Redis: {e}")

    def set_value(self, key, value, ttl=None):
        """
        設置一個鍵值對，並選擇性地設置 TTL。

        :param key: 鍵
        :param value: 值
        :param ttl: 鍵的存活時間（秒），默認為 None
        """
        try:
            if ttl:
                self.client.setex(key, ttl, value)
                print(f"Set {key} = {value} with TTL {ttl} seconds")
            else:
                self.client.set(key, value)
                print(f"Set {key} = {value}")
        except Exception as e:
            print(f"Failed to set {key}: {e}")

    def get_value(self, key):
        """
        獲取一個鍵的值。

        :param key: 鍵
        :return: 鍵的值，如果鍵不存在則返回 None
        """
        try:
            value = self.client.get(key)
            print(f"Get {key} = {value}")
            return value
        except Exception as e:
            print(f"Failed to get {key}: {e}")
            return None

    def delete_value(self, key):
        """
        刪除一個鍵。

        :param key: 鍵
        """
        try:
            self.client.delete(key)
            print(f"Deleted {key}")
        except Exception as e:
            print(f"Failed to delete {key}: {e}")

    def exists(self, key):
        """
        檢查一個鍵是否存在。

        :param key: 鍵
        :return: 如果鍵存在則返回 True，否則返回 False
        """
        try:
            exists = self.client.exists(key)
            print(f"{key} exists: {exists}")
            return exists
        except Exception as e:
            print(f"Failed to check if {key} exists: {e}")
            return False

# 從 .env 文件中讀取 Redis 配置
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)

# 全局 Redis 連接實例
redis_engine = RedisEngine(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)

# 測試 RedisEngine
if __name__ == "__main__":
    redis_engine.set_value('test_key', 'test_value', ttl=60)  # 設置有 TTL 的鍵值對
    redis_engine.get_value('test_key')
    redis_engine.exists('test_key')
    redis_engine.delete_value('test_key')
    redis_engine.exists('test_key')

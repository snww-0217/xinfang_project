from django_redis import get_redis_connection
from django.core.exceptions import ImproperlyConfigured
import json


class RedisClient:
    """Redis 客户端封装"""

    def __init__(self, alias='default'):
        """初始化 Redis 连接"""
        self.connection = get_redis_connection(alias)

    def get(self, key, default=None):
        """获取缓存数据（自动反序列化）"""
        value = self.connection.get(key)
        if value is None:
            return default
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value.decode('utf-8')

    def set(self, key, value, expire=None):
        """设置缓存数据（自动序列化）"""
        if isinstance(value, (dict, list)):
            value = json.dumps(value)
        self.connection.set(key, value, ex=expire)

    def delete(self, key):
        """删除缓存数据"""
        self.connection.delete(key)

    def increment(self, key, amount=1):
        """递增 key 的值"""
        return self.connection.incr(key, amount)

    def exists(self, key):
        """检查 key 是否存在"""
        return self.connection.exists(key)

    def flush_db(self):
        """清空数据库（慎用！）"""
        self.connection.flushdb()

    def get_ttl(self, key):
        """获取 key 的剩余生存时间（TTL）"""
        return self.connection.ttl(key)


# 单例模式，避免重复创建连接
redis_client = RedisClient()


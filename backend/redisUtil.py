# utils/redisUtil.py
import redis
redis_pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    db=0,
    password=None,
    decode_responses=True
)
redis_client = redis.Redis(connection_pool=redis_pool)
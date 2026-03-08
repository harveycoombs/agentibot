import os
import redis

rc = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=0)

def get_kv(key):
    try:
        return rc.get(key)
    except Exception as e:
        print(f"Unable to get KV pair: {e}")
        return None

def set_kv(key, value):
    try:
        rc.set(key, value)
    except Exception as e:
        print(f"Unable to set KV pair: {e}")
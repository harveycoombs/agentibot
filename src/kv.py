import os
import redis

rc = redis.Redis(host=os.getenv("REDIS_HOST"), port=os.getenv("REDIS_PORT"), db=0) if os.getenv("REDIS_HOST") and os.getenv("REDIS_PORT") else None

def get_kv(key):
    if not rc:
        return None

    try:
        return rc.get(key)
    except Exception as e:
        print(f"Unable to get KV pair: {e}")
        return None

def set_kv(key, value):
    if not rc:
        return

    try:
        rc.set(key, value)
    except Exception as e:
        print(f"Unable to set KV pair: {e}")
"""
Clear Redis cache for development reset.
"""
import redis
from shared.config.settings import settings

def run():
    print("🗑 Clearing Redis cache...")
    r = redis.from_url(settings.REDIS_URL or "redis://localhost:6379/0")
    r.flushall()
    print("✅ Redis cache cleared.")

if __name__ == "__main__":
    run()

import redis
import os
from urllib.parse import urlparse

# Retrieve the Redis connection string
redis_url = os.getenv("REDIS_URL")

if redis_url:
    # Parse the connection string
    result = urlparse(redis_url)
    redis_host = result.hostname
    redis_port = result.port
    redis_password = result.password
else:
    # Fallback values for local development
    redis_host = os.getenv("REDIS_HOST", "localhost")
    redis_port = int(os.getenv("REDIS_PORT", 6379))
    redis_password = None

# Create the Redis client
redis_client = redis.StrictRedis(
    host=redis_host,
    port=redis_port,
    password=redis_password,
    db=0
)
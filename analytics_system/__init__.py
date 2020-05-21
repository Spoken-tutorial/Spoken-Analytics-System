
import redis
# Initialize redis client
REDIS_CLIENT = redis.Redis(
    host='localhost',
    port=6379,
    db=0
)

# Create and configure the pymongo client
from pymongo import MongoClient

MONGO_CLIENT = MongoClient()

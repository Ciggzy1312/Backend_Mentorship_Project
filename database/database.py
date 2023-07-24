import os
from dotenv import load_dotenv
from motor import motor_asyncio
import redis

load_dotenv()
client = motor_asyncio.AsyncIOMotorClient(os.environ["DB_URL"])

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

try:
    print("Connected to MongoDB and Redis")
except Exception:
    print("Unable to connect to MongoDB or Redis")

db = client.Mentorship_Project
User = db.user
Product = db.product
Basket = db.basket
Order = db.order
import os
from dotenv import load_dotenv
from motor import motor_asyncio

load_dotenv()
client = motor_asyncio.AsyncIOMotorClient(os.environ["DB_URL"])

try:
    print("Connected to MongoDB")
except Exception:
    print("Unable to connect to MongoDB")

db = client.Mentorship_Project
User = db.user
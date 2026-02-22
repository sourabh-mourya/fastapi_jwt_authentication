from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

if not MONGO_URI:
    raise Exception("MONGO_URI is not set in .env")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]
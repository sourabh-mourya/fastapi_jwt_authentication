from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME")

if not MONGO_URI:
    raise Exception("MONGO_URI is missing in .env file")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

# Connection test karne ke liye function (Optional but good)
async def check_db():
    try:
        await client.admin.command('ping')
        print("✅ MongoDB connected successfully!")
    except Exception as e:
        print(f"❌ MongoDB connection failed: {e}")
# database.py
import motor.motor_asyncio
import os
from dotenv import load_dotenv
from pymongo.errors import ConnectionFailure

# Load environment variables from a .env file (optional, if you use it)
load_dotenv()

# Retrieve the MongoDB URI from environment variables
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

# Create an AsyncIOMotorClient
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)

# Get the database
db = client.get_database('school_blog')

# Test the connection
try:
    # Attempt to ping the database
    client.admin.command('ping')
    print("Successfully connected to MongoDB")
except ConnectionFailure as e:
    print(f"Failed to connect to MongoDB: {e}")
    raise

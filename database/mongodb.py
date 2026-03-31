from pymongo import MongoClient
from config.settings import MONGO_URL

client = MongoClient(MONGO_URL)

db = client["machi_ai"]

users = db["users"]
messages = db["messages"]
business_accounts = db["business_accounts"]
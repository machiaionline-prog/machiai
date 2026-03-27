from pymongo import MongoClient
from config import MONGO_URL

client = MongoClient(MONGO_URL)
db = client["machi_ai"]

def get_user_style(user_id):

    user = db.users.find_one({"user": user_id})

    if user:
        return user["style"]

    return "casual tamil english chat"

def save_user_style(user_id, style):

    db.users.update_one(
        {"user": user_id},
        {"$set": {"style": style}},
        upsert=True
    )
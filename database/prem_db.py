from pymongo import MongoClient
import os
from datetime import datetime, timedelta

# Database setup
client = MongoClient(os.getenv("MONGODB_URI"))
db = client['file_bot']
premium_users = db['premium_users']

def add_premium_user(user_id, duration):
    expiry_date = datetime.now() + timedelta(days=duration)
    premium_users.update_one(
        {'user_id': user_id},
        {'$set': {'expiry_date': expiry_date}},
        upsert=True
    )

def remove_premium_user(user_id):
    premium_users.delete_one({'user_id': user_id})

def get_premium_users():
    return list(premium_users.find({}))

def is_premium(user_id):
    user = premium_users.find_one({'user_id': user_id})
    return user and user['expiry_date'] > datetime.now()

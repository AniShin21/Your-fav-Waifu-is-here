import motor.motor_asyncio
from datetime import datetime, timedelta
from config import DB_URL, DB_NAME

# Initialize the MongoDB client
dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
database = dbclient[DB_NAME]

# Collection for storing premium user data
premium_data = database['premium_users']

# Default values for premium user data
default_premium = {
    'user_id': 0,
    'expiry_date': 0,
    'subscription_duration': 0  # Duration in days
}

# Function to create a new premium user document
def new_premium_user(user_id: int, duration: int):
    return {
        'user_id': user_id,
        'expiry_date': (datetime.now() + timedelta(days=duration)).timestamp(),
        'subscription_duration': duration
    }

# Function to add a new premium user or update an existing one
async def add_premium_user(user_id: int, duration: int):
    premium_user = new_premium_user(user_id, duration)
    await premium_data.update_one({'user_id': user_id}, {'$set': premium_user}, upsert=True)

# Function to remove a premium user
async def remove_premium_user(user_id: int):
    await premium_data.delete_one({'user_id': user_id})

# Function to check if a user is premium and if their subscription is still valid
async def is_premium(user_id: int):
    user = await premium_data.find_one({'user_id': user_id})
    return bool(user) and user['expiry_date'] > datetime.now().timestamp()

# Function to get all premium users
async def get_premium_users():
    users = await premium_data.find().to_list(length=1000)  # Adjust the length as needed
    return users

# Function to get a premium user's details
async def get_premium_user_details(user_id: int):
    user = await premium_data.find_one({'user_id': user_id})
    return user

# Function to check for expired premium users
async def check_expired_premiums():
    current_time = datetime.now().timestamp()
    expired_users = premium_data.find({'expiry_date': {'$lt': current_time}})
    return [user async for user in expired_users]

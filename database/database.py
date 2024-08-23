import motor.motor_asyncio
from config import DB_URL, DB_NAME

dbclient = motor.motor_asyncio.AsyncIOMotorClient(DB_URL)
database = dbclient[DB_NAME]

# Collection for user data
user_data = database['users']

# Collection for storing premium user data

# Default values for user verification status
default_verify = {
    'is_verified': False,
    'verified_time': 0,
    'verify_token': "",
    'link': ""
}


def new_user(id):
    return {
        '_id': id,
        'verify_status': {
            'is_verified': False,
            'verified_time': "",
            'verify_token': "",
            'link': ""
        }
    }

async def present_user(user_id: int):
    found = await user_data.find_one({'_id': user_id})
    return bool(found)

async def add_user(user_id: int):
    user = new_user(user_id)
    await user_data.insert_one(user)
    return

async def db_verify_status(user_id):
    user = await user_data.find_one({'_id': user_id})
    if user:
        return user.get('verify_status', default_verify)
    return default_verify

async def db_update_verify_status(user_id, verify):
    await user_data.update_one({'_id': user_id}, {'$set': {'verify_status': verify}})

async def full_userbase():
    user_docs = user_data.find()
    user_ids = [doc['_id'] async for doc in user_docs]
    return user_ids

async def del_user(user_id: int):
    await user_data.delete_one({'_id': user_id})
    return

#################  Database Pagal hai mat suno uss ki baat tum ##################
async def get_premium_status(user_id):
    user = await db.premium_users.find_one({"user_id": user_id})
    if user and user["expiry_date"] > datetime.utcnow():
        return True
    return False

async def add_premium_user(user_id, duration):
    expiry_date = datetime.utcnow() + timedelta(seconds=duration)
    await db.premium_users.update_one(
        {"user_id": user_id},
        {"$set": {"expiry_date": expiry_date}},
        upsert=True
    )

async def remove_premium_user(user_id):
    await db.premium_users.delete_one({"user_id": user_id})

async def get_premium_users():
    users = await db.premium_users.find({"expiry_date": {"$gt": datetime.utcnow()}}).to_list(None)
    return users

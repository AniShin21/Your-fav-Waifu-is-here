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

default_verify = False


# MongoDB Utility Functions
async def db_verify_status(user_id):
    """Get the verification status of a user."""
    user = await user_data.find_one({'_id': user_id})
    if user:
        return user.get('verify_status', default_verify)
    return default_verify


async def db_add_verified_user(user_id, username=None, first_name=None, last_name=None):
    """Add a user to the verified_users collection."""
    existing_user = await user_data.find_one({'_id': user_id})
    if existing_user:
        return False  # User already exists
    await user_data.insert_one({
        '_id': user_id,
        'username': username,
        'first_name': first_name,
        'last_name': last_name,
        'verify_status': True
    })
    return True


async def db_is_already_verified(user_id):
    """Check if a user is already verified."""
    user = await user_data.find_one({'_id': user_id})
    return user is not None


async def db_get_all_verified_users():
    """Get all verified users."""
    users = await user_data.find({'verify_status': True}).to_list(length=None)
    return users

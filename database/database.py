import pymongo
import os
from config import DB_URL, DB_NAME


dbclient = pymongo.MongoClient(DB_URL)
database = dbclient[DB_NAME]


user_data = database['users']


async def present_user(user_id: int):
    found = user_data.find_one({'_id': user_id})
    return bool(found)


async def add_user(user_id: int):
    user_data.insert_one({'_id': user_id})
    return


async def full_userbase():
    user_docs = user_data.find()
    user_ids = []
    for doc in user_docs:
        user_ids.append(doc['_id'])

    return user_ids


async def del_user(user_id: int):
    user_data.delete_one({'_id': user_id})
    return

# Admins Database
async def present_admin(user_id: int):
    found = await admin_data.find_one({'_id': user_id})
    return bool(found)


async def add_admin(user_id: int):
    user = new_user(user_id)
    await admin_data.insert_one(user)
    ADMINS.append(int(user_id))
    return

async def del_admin(user_id: int):
    await admin_data.delete_one({'_id': user_id})
    ADMINS.remove(int(user_id))
    return

async def full_adminbase():
    user_docs = admin_data.find()
    user_ids = [int(doc['_id']) async for doc in user_docs]
    return user_ids

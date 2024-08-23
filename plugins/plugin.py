from pyrogram import filters
from pyrogram.types import Message
from bot import Bot
from database.database import get_premium_users, add_premium_user, remove_premium_user
from helper_func import get_exp_time
from config import ADMINS

# Command to add a user to the premium list
@Bot.on_message(filters.command("add_premium") & filters.user(ADMINS))
async def add_premium(client, message: Message):
    try:
        user_id = int(message.command[1])
        duration = int(message.command[2])  # Duration in seconds
        await add_premium_user(user_id, duration)
        await message.reply_text(f"User {user_id} has been added as a premium user for {get_exp_time(duration)}.")
    except (IndexError, ValueError):
        await message.reply_text("Usage: /add_prem <user_id> <duration_in_seconds>")

# Command to remove a user from the premium list
@Bot.on_message(filters.command("remove_premium") & filters.user(ADMINS))
async def remove_premium(client, message: Message):
    try:
        user_id = int(message.command[1])
        await remove_premium_user(user_id)
        await message.reply_text(f"User {user_id} has been removed from premium.")
    except (IndexError, ValueError):
        await message.reply_text("Usage: /remove_prem <user_id>")

# Command to list all current premium users
@Bot.on_message(filters.command("premium_users") & filters.user(ADMINS))
async def list_premium_users(client, message: Message):
    users = await get_premium_users()
    if users:
        reply = "Premium Users:\n"
        for user in users:
            expiry_time = user['expiry_date'].timestamp() - message.date.timestamp()
            reply += f"User ID: {user['user_id']}, Expires in: {get_exp_time(expiry_time)}\n"
        await message.reply_text(reply)
    else:
        await message.reply_text("No premium users found.")

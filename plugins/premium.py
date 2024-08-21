import asyncio
from pyrogram import filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime, timedelta
from bot import Bot  # Import your Bot instance
from database.premium_database import add_premium_user, remove_premium_user, is_premium, get_premium_users
from config import ADMINS



@Bot.on_message(filters.command('add_premium') & filters.private & filters.user(ADMINS))
async def add_premium(client: Bot, message: Message):
    if len(message.command) != 3:
        await message.reply("Usage: /add_premium [user_id] [duration_in_days]")
        return

    user_id = int(message.command[1])
    duration = int(message.command[2])

    await add_premium_user(user_id, duration)
    await message.reply(f"User {user_id} has been added to premium for {duration} days.")

@Bot.on_message(filters.command('remove_premium') & filters.private & filters.user(ADMINS))
async def remove_premium(client: Bot, message: Message):
    if len(message.command) != 2:
        await message.reply("Usage: /remove_premium [user_id]")
        return

    user_id = int(message.command[1])
    await remove_premium_user(user_id)
    await message.reply(f"User {user_id} has been removed from premium.")

@Bot.on_message(filters.command('check_premium') & filters.private)
async def check_premium(client: Bot, message: Message):
    user_id = message.from_user.id
    premium_status = await is_premium(user_id)

    if premium_status:
        await message.reply("You are a premium user!")
    else:
        await message.reply("You are not a premium user.")

async def notify_expired_premium_users(client: Bot):
    while True:
        users = await get_premium_users()
        current_time = datetime.now().timestamp()
        
        for user in users:
            if user['expiry_date'] < current_time:
                try:
                    await client.send_message(
                        chat_id=user['user_id'],
                        text="Your premium membership has expired. Please contact the admin to renew."
                    )
                    # Remove the user from premium
                    await remove_premium_user(user['user_id'])
                except Exception as e:
                    print(f"Failed to notify user {user['user_id']} about premium expiration: {e}")

        await asyncio.sleep(3600)  # Check every hour

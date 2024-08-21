import asyncio
from datetime import datetime, timedelta
from pyrogram import filters
from pyrogram.types import Message
from bot import Bot
from config import ADMINS, OWNER
from database.database import add_premium_user, remove_premium_user, is_premium, get_premium_users

# Add a user to premium
@Bot.on_message(filters.command('add_prem') & filters.private & filters.user(ADMINS))
async def add_prem_command(client: Bot, message: Message):
    if len(message.command) != 3:
        await message.reply("Usage: /add_prem <user_id> <duration_in_days>")
        return

    user_id = int(message.command[1])
    duration = int(message.command[2])

    # Check if the user is present in the bot
    if not await is_premium(user_id):
        await add_premium_user(user_id, duration)
        await message.reply(f"User {user_id} has been added to premium for {duration} days.")
    else:
        await message.reply(f"User {user_id} is already a premium user.")

# Remove a user from premium
@Bot.on_message(filters.command('remove_prem') & filters.private & filters.user(ADMINS))
async def remove_prem_command(client: Bot, message: Message):
    if len(message.command) != 2:
        await message.reply("Usage: /remove_prem <user_id>")
        return

    user_id = int(message.command[1])

    # Check if the user is premium
    if await is_premium(user_id):
        await remove_premium_user(user_id)
        await message.reply(f"User {user_id} has been removed from premium.")
    else:
        await message.reply(f"User {user_id} is not a premium user.")

# Check premium status of a user
@Bot.on_message(filters.command('check_prem') & filters.private & filters.user(ADMINS))
async def check_prem_command(client: Bot, message: Message):
    if len(message.command) != 2:
        await message.reply("Usage: /check_prem <user_id>")
        return

    user_id = int(message.command[1])

    # Check if the user is premium
    if await is_premium(user_id):
        await message.reply(f"User {user_id} is a premium user.")
    else:
        await message.reply(f"User {user_id} is not a premium user.")

# List all premium users
@Bot.on_message(filters.command('all_prems') & filters.private & filters.user(ADMINS))
async def all_prems_command(client: Bot, message: Message):
    users = await get_premium_users()
    if users:
        user_list = "\n".join([f"User ID: {user['user_id']}, Expiry: {datetime.fromtimestamp(user['expiry_date']).strftime('%Y-%m-%d %H:%M:%S')}" for user in users])
        await message.reply(f"List of all premium users:\n\n{user_list}")
    else:
        await message.reply("No premium users found.")

# Notify user and owner when membership expires
async def notify_expired_premium_users(client: Bot):
    while True:
        current_time = datetime.now().timestamp()
        users = await get_premium_users()

        for user in users:
            if user['expiry_date'] <= current_time:
                user_id = user['user_id']

                # Notify the user
                try:
                    await client.send_message(
                        chat_id=user_id,
                        text="Hey Dude, What's Up\n\nYour membership has expired. For more info, contact Owner or Admins."
                    )
                except Exception as e:
                    print(f"Failed to notify user {user_id}: {e}")

                # Notify the owner
                try:
                    await client.send_message(
                        chat_id=OWNER,
                        text=f"Hello My Hot Owner\n\nThe membership of user {user_id} has expired."
                    )
                except Exception as e:
                    print(f"Failed to notify owner about user {user_id}: {e}")

                # Remove user from premium
                await remove_premium_user(user_id)

        await asyncio.sleep(3600)  # Check every hour

# Start the notification task when the bot starts
@Bot.on_start
async def start_notification_task(client: Bot):
    client.loop.create_task(notify_expired_premium_users(client))

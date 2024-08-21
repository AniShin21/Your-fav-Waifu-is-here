import asyncio
from datetime import datetime
from pyrogram import filters
from bot import Bot
from config import ADMINS
from premium_database import add_premium_user, remove_premium_user, get_premium_users, is_premium

async def notify_expired_premium_users(client: Bot):
    while True:
        # Check for expired users every hour (or any other interval)
        await asyncio.sleep(3600)  # 1 hour
        
        premium_users = await get_premium_users()
        now = datetime.now().timestamp()
        
        for user in premium_users:
            if user['expiry_date'] < now:
                # Notify the user
                try:
                    await client.send_message(user['user_id'], "Your premium membership has expired.")
                except Exception as e:
                    print(f"Failed to notify user {user['user_id']}: {e}")
                
                # Remove the expired user from premium
                await remove_premium_user(user['user_id'])
                
                # Notify the owner
                try:
                    owner_id = ADMINS  # Replace with the actual owner ID or list
                    await client.send_message(owner_id, f"Premium membership expired for user: {user['user_id']}")
                except Exception as e:
                    print(f"Failed to notify owner about user {user['user_id']}: {e}")

@Bot.on_message(filters.command('add_premium') & filters.private & filters.user(ADMINS))
async def add_premium(client: Bot, message: Message):
    try:
        user_id = int(message.command[1])
        duration = int(message.command[2])  # Duration in days
        await add_premium_user(user_id, duration)
        await message.reply(f"Added premium for user {user_id} for {duration} days.")
    except IndexError:
        await message.reply("Usage: /add_premium <user_id> <duration_in_days>")
    except ValueError:
        await message.reply("Invalid user ID or duration. Please provide valid integers.")

@Bot.on_message(filters.command('remove_premium') & filters.private & filters.user(ADMINS))
async def remove_premium(client: Bot, message: Message):
    try:
        user_id = int(message.command[1])
        await remove_premium_user(user_id)
        await message.reply(f"Removed premium for user {user_id}.")
    except IndexError:
        await message.reply("Usage: /remove_premium <user_id>")
    except ValueError:
        await message.reply("Invalid user ID. Please provide a valid integer.")

@Bot.on_message(filters.command('list_premium') & filters.private & filters.user(ADMINS))
async def list_premium_users(client: Bot, message: Message):
    premium_users = await get_premium_users()
    if not premium_users:
        await message.reply("No premium users found.")
        return

    response = "List of premium users:\n\n"
    for user in premium_users:
        response += f"User ID: {user['user_id']}, Expiry Date: {datetime.fromtimestamp(user['expiry_date']).strftime('%Y-%m-%d %H:%M:%S')}, Duration: {user['subscription_duration']} days\n"

    await message.reply(response)

@Bot.on_message(filters.command('check_premium') & filters.private)
async def check_premium_status(client: Bot, message: Message):
    user_id = message.from_user.id
    if await is_premium(user_id):
        premium_user = await premium_data.find_one({'user_id': user_id})
        expiry_date = datetime.fromtimestamp(premium_user['expiry_date']).strftime('%Y-%m-%d %H:%M:%S')
        await message.reply(f"Your premium membership is active. Expiry Date: {expiry_date}.")
    else:
        await message.reply("You are not a premium user.")

# Note: Ensure 'notify_expired_premium_users' is started in the main script or another suitable place.

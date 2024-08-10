import os
import asyncio
from pyrogram import Client, filters, __version__
from pyrogram.enums import ParseMode
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from config import ADMINS, OWNER
from database.database import add_premium_user, remove_premium_user, get_premium_users, is_premium, present_user
from bot import Bot
# Command to add a premium user
@Bot.on_message(filters.private & filters.command('add_prem') & filters.user(ADMINS))
async def add_premium(client: Bot, message: Message):
    # Ask for the user ID
    try:
        user_id_msg = await client.ask(
            chat_id=message.chat.id,
            text="Please enter the user ID:",
            timeout=60
        )
        user_id = int(user_id_msg.text)

        # Check if the user has ever used the bot
        if not await present_user(user_id):
            await message.reply("User not found in the bot.")
            return

        # Ask for the subscription duration
        duration_msg = await client.ask(
            chat_id=message.chat.id,
            text="Choose the subscription duration:\n1 week, 1 month, 3 months, 6 months, 12 months, or 1 minute for testing.",
            timeout=60
        )
        duration = duration_msg.text.lower()

        # Convert duration to days
        if duration == '1 week':
            duration_days = 7
        elif duration == '1 month':
            duration_days = 30
        elif duration == '3 months':
            duration_days = 90
        elif duration == '6 months':
            duration_days = 180
        elif duration == '12 months':
            duration_days = 365
        elif duration == '1 minute':
            duration_days = 1/1440  # 1 minute
        else:
            await message.reply("Invalid duration entered.")
            return

        # Add the user to premium
        await add_premium_user(user_id, duration_days)
        await message.reply(f"User {user_id} has been added to premium for {duration}.")
    except asyncio.TimeoutError:
        await message.reply("⏳ Time ran out. Please try again.")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

# Command to remove a premium user
@Bot.on_message(filters.private & filters.command('remove_prem') & filters.user(ADMINS))
async def remove_premium(client: Bot, message: Message):
    try:
        user_id_msg = await client.ask(
            chat_id=message.chat.id,
            text="Please enter the user ID to remove from premium:",
            timeout=60
        )
        user_id = int(user_id_msg.text)

        # Remove the user from premium
        await remove_premium_user(user_id)
        await message.reply(f"User {user_id} has been removed from premium.")
    except asyncio.TimeoutError:
        await message.reply("⏳ Time ran out. Please try again.")
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

# Command to list all premium users
@Bot.on_message(filters.private & filters.command('all_prems') & filters.user(ADMINS))
async def list_premium_users(client: Bot, message: Message):
    premium_users = await get_premium_users()

    if not premium_users:
        await message.reply("No premium users found.")
        return

    text = "<b>Premium Users:</b>\n\n"
    for user in premium_users:
        user_id = user['user_id']
        expiry_date = datetime.fromtimestamp(user['expiry_date']).strftime('%Y-%m-%d %H:%M:%S')
        text += f"User ID: <code>{user_id}</code>\nExpiry Date: {expiry_date}\n\n"

    await message.reply(text, parse_mode=ParseMode.HTML)

# Task to check for expired premium memberships
async def check_expired_premiums():
    while True:
        premium_users = await get_premium_users()
        current_time = datetime.now().timestamp()

        for user in premium_users:
            if user['expiry_date'] < current_time:
                user_id = user['user_id']

                # Notify the user about their expired membership
                try:
                    await Bot.send_message(
                        chat_id=user_id,
                        text="Hey Dude What's Up\n\nYour membership is expired. For more info contact Owner or Admins."
                    )
                except Exception as e:
                    print(f"Failed to notify user {user_id}: {e}")

                # Notify the owner about the expired membership
                try:
                    await Bot.send_message(
                        chat_id=OWNER,
                        text=f"Hello My Hot Owner\n\nThis Person ({user_id})'s membership is expired. So I am informing you."
                    )
                except Exception as e:
                    print(f"Failed to notify owner about user {user_id}: {e}")

                # Remove the user from premium
                await remove_premium_user(user_id)

        # Sleep for a while before checking again
        await asyncio.sleep(3600)  # Check every hour

# Start the task to check for expired premiums
Bot.loop.create_task(check_expired_premiums())

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.errors import UserNotParticipant
from config import ADMINS, OWNER_ID
from database.prem_db import add_premium_user, remove_premium_user, get_premium_users, is_premium
from datetime import datetime
from bot import Bot
import asyncio

@Bot.on_message(filters.command('add_prem') & filters.private & filters.user(ADMINS))
async def add_prem_user(client: Client, message: Message):
    await message.reply_text("Please provide the user ID to add to premium:")
    response = await client.listen(message.chat.id, filters=filters.text)

    user_id = int(response.text.strip())

    # Check if the user is currently using the bot
    try:
        await client.get_chat_member(message.chat.id, user_id)
        # If the user is found, proceed to add them to premium
        buttons = [
            [InlineKeyboardButton("1 Week", callback_data=f"add_prem:{user_id}:7")],
            [InlineKeyboardButton("1 Month", callback_data=f"add_prem:{user_id}:30")],
            [InlineKeyboardButton("3 Months", callback_data=f"add_prem:{user_id}:90")],
            [InlineKeyboardButton("6 Months", callback_data=f"add_prem:{user_id}:180")],
            [InlineKeyboardButton("12 Months", callback_data=f"add_prem:{user_id}:365")],
            [InlineKeyboardButton("1 Minute (Test)", callback_data=f"add_prem:{user_id}:1")]
        ]
        
        await message.reply_text(
            "Select the duration for premium membership:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    except UserNotParticipant:
        await message.reply_text("User Not Found in Bot")

@Bot.on_callback_query(filters.regex(r"^add_prem:(\d+):(\d+)$") & filters.user(ADMINS))
async def on_add_prem_callback(client: Client, callback_query):
    user_id, duration = map(int, callback_query.data.split(":")[1:])
    add_premium_user(user_id, duration)
    await callback_query.answer(f"User {user_id} added to premium for {duration} days!")

    # Notify the owner about the addition
    owner_message = f"Hello My Hot Owner\n\nThis Person ({user_id})'s membership has been added for {duration} days."
    await client.send_message(OWNER_ID, owner_message)

@Bot.on_message(filters.command('remove_prem') & filters.private & filters.user(ADMINS))
async def remove_prem_user(client: Client, message: Message):
    await message.reply_text("Please provide the user ID to remove from premium:")
    response = await client.listen(message.chat.id, filters=filters.text)

    user_id = int(response.text.strip())
    remove_premium_user(user_id)
    await message.reply_text(f"User {user_id} removed from premium.")

    # Notify the owner about the removal
    owner_message = f"Hello My Hot Owner\n\nThis Person ({user_id})'s membership has been removed."
    await client.send_message(OWNER_ID, owner_message)

@Bot.on_message(filters.command('all_prems') & filters.private & filters.user(ADMINS))
async def all_prems(client: Client, message: Message):
    users = get_premium_users()
    if not users:
        await message.reply_text("No premium users found.")
        return

    response = "List of all premium users and their stats:\n\n"
    for user in users:
        user_id = user['user_id']
        user_name = (await client.get_users(user_id)).full_name
        expiry_date = user['expiry_date'].strftime("%Y-%m-%d %H:%M:%S")
        response += f"User: {user_name} (ID: {user_id})\nExpires: {expiry_date}\n\n"

    await message.reply_text(response)

# Check for expired memberships and notify users and owner
async def check_expired_memberships(client: Client):
    users = get_premium_users()
    for user in users:
        if user['expiry_date'] < datetime.now():
            user_id = user['user_id']
            user_name = (await client.get_users(user_id)).full_name  # Get the user's name
            # Notify the user
            user_message = "Hey Dude What's Up\n\nYour membership is expired. For more info, contact the Owner or Admins."
            try:
                await client.send_message(user_id, user_message)
            except:
                pass  # If user is not found, handle it gracefully

            # Notify the owner with the user's name
            owner_message = f"Hello My Hot Owner\n\nThis Person ({user_name} - {user_id})'s membership has expired."
            await client.send_message(OWNER_ID, owner_message)

            # Automatically remove the expired membership
            remove_premium_user(user_id)

# Schedule the membership check (e.g., every hour)
async def schedule_membership_check(client: Client):
    while True:
        await check_expired_memberships(client)
        await asyncio.sleep(3600)  # Check every hour



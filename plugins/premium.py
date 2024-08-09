from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from datetime import datetime
from config import ADMINS
from bot import Bot

# Import functions from database script
from database import add_premium_user, remove_premium_user, get_premium_users, is_premium
from config import ADMINS

@Bot.on_message(filters.command('add_prem') & filters.private & filters.user(ADMINS))
async def add_prem_user(client: Bot, message: Message):
    await message.reply_text("Please provide the user ID to add to premium:")
    response = await client.listen(message.chat.id, filters=filters.text)

    user_id = int(response.text.strip())
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

@Bot.on_callback_query(filters.regex(r"^add_prem:(\d+):(\d+)$") & filters.user(ADMINS))
async def on_add_prem_callback(client: Bot, callback_query):
    user_id, duration = map(int, callback_query.data.split(":")[1:])
    add_premium_user(user_id, duration)
    await callback_query.answer(f"User {user_id} added to premium for {duration} days!")

@Bot.on_message(filters.command('remove_prem') & filters.private & filters.user(ADMINS))
async def remove_prem_user(client: Bot, message: Message):
    await message.reply_text("Please provide the user ID to remove from premium:")
    response = await client.listen(message.chat.id, filters=filters.text)

    user_id = int(response.text.strip())
    remove_premium_user(user_id)
    await message.reply_text(f"User {user_id} removed from premium.")

@Bot.on_message(filters.command('prem_users') & filters.private & filters.user(ADMINS))
async def list_prem_users(client: Bot, message: Message):
    users = get_premium_users()
    if not users:
        await message.reply_text("No premium users found.")
        return

    for user in users:
        user_details = f"User ID: {user['user_id']}\nExpiry: {user['expiry_date'].strftime('%Y-%m-%d %H:%M:%S')}"
        button = InlineKeyboardButton("Show Details", callback_data=f"show_prem_details:{user['user_id']}")
        await message.reply_text(user_details, reply_markup=InlineKeyboardMarkup([[button]]))

@Bot.on_callback_query(filters.regex(r"^show_prem_details:(\d+)$") & filters.user(ADMINS))
async def on_show_prem_details(client: Bot, callback_query):
    user_id = int(callback_query.data.split(":")[1])
    user = premium_users.find_one({'user_id': user_id})
    if user:
        details = f"User ID: {user['user_id']}\nExpiry: {user['expiry_date'].strftime('%Y-%m-%d %H:%M:%S')}"
        await callback_query.answer(details, show_alert=True)
    else:
        await callback_query.answer("User not found in premium.", show_alert=True)


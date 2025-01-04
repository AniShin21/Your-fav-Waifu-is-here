import random
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.enums import ParseMode
from database.database import full_userbase  # Assuming you have a collection for users
from config import ADMINS
from bot import Bot
# Assuming Bot is your pyrogram Client instance
@Bot.on_message(filters.command("win") & filters.private & filters.user(ADMINS))
async def win_command(bot: Client, message: Message):
    try:
        # Extract the number of winners from the message
        args = message.text.split()
        if len(args) != 2 or not args[1].isdigit():
            await message.reply("Please specify the number of winners in the format: /win <number>")
            return
        
        num_winners = int(args[1])

        # Fetch all users from the database (assuming full_userbase function gets all users)
        users = await db_get_all_verified_users()

        if len(users) < num_winners:
            await message.reply("Not enough users in the database to select that many winners.")
            return

        # Randomly select winners
        winners = random.sample(users, num_winners)

        # Prepare a cool font for the winner details
        winner_details = ""
        for winner in winners:
            username = winner.get("username", "N/A")
            user_id = winner.get("user_id")
            first_name = winner.get("first_name", "No Name")
            last_name = winner.get("last_name", "")
            winner_details += f"""
            🎉 **Winner** 🎉
            **Username**: @{username if username != "N/A" else "No Username"}
            **Name**: {first_name} {last_name}
            **User ID**: {user_id}
            -------------------------
            """

        # Send the winners' details in a cool style
        await message.reply(winner_details, parse_mode=ParseMode.MARKDOWN)
    
    except Exception as e:
        await message.reply(f"An error occurred: {e}")

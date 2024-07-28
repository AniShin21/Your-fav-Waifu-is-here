from pyrogram import __version__
from bot import Bot
from config import OWNER_ID
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery


@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        await query.message.edit_text(
            text=f"<b>╭━━━━━━━━━━━━━━━➣\n┣⪼ Owner : <a href='tg://user?id=5745818770'>Vergil</a>\n┣⪼ Bot Updates : <a href'https://t.me/ikigai_bots'>IKigai</a>\n┣⪼ Support Channel: <a href='https://t.me/ikigai_chats'>Ikigai Support</a>\n┣⪼ Our Network :<a href='https://t.me/ikigai_Network'>Ikigai Network</a>\n┣⪼ Movies Channel :<a href='https://t.me/ikigai_Movies'>Ikigai Movies</a>\n╰───────────────⍟</b>",
            disable_web_page_preview=True,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data="close")
                    ]
                ]
            )
        )
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

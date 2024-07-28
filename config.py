import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from pymongo import MongoClient
import pymongo
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import requests

response = requests.get('https://api.ipify.org?format=json')
ip = response.json()['ip']
print(f'Public IP Address: {ip}')


# Load the .env file
load_dotenv()

TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
APP_ID = int(os.environ.get("APP_ID", "28196802"))
API_HASH = os.environ.get("API_HASH", "dccf92fd1c0bad1b7de1e8efc63654ff")


OWNER = os.environ.get("OWNER", "@VergilGfx")  # Owner username
OWNER_ID = int(os.environ.get("OWNER_ID", "5745818770"))  # Owner user id
DB_URL = os.environ.get("DB_URL", "")
DB_NAME = os.environ.get("DB_NAME", "")


CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002215036092"))
FORCE_SUB_CHANNEL1 = int(os.environ.get("FORCE_SUB_CHANNEL1", "0"))
FORCE_SUB_CHANNEL2 = int(os.environ.get("FORCE_SUB_CHANNEL2", "0"))
FORCE_SUB_CHANNEL3 = int(os.environ.get("FORCE_SUB_CHANNEL3", "0"))


SECONDS = int(os.getenv("SECONDS", "600"))  # auto delete in seconds


PORT = os.environ.get("PORT", "8080")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "5"))


# start message
START_MSG = os.environ.get(
    "START_MESSAGE", "<b><i>Hᴇʟʟᴏ Tʜᴇʀᴇ {mention} Dᴀʀʟɪɴɢ 👋\n\nI sᴛᴀʏ ᴜᴘ ᴀʟʟ ɴɪɢʜᴛ ᴛᴏ ғᴜʟғɪʟʟ ʏᴏᴜʀ ғᴀɴᴛᴀsɪᴇs 🫦✨</i></b>")

try:
    ADMINS = [5745818770]
    for x in (os.environ.get("ADMINS", "5745818770 5964367469 7138310520 6877704277 1207296799").split()):
        ADMINS.append(int(x))
except ValueError:
    raise Exception("Your Admins list does not contain valid integers.")


FORCE_MSG = os.environ.get(
    "FORCE_SUB_MESSAGE", "<b><center>Hey {first}</center></b>\n𝖩𝗈𝗂𝗇 𝖬𝗒 𝖡𝖺𝖼𝗄𝗎𝗉 𝖢𝗁𝖺𝗇𝗇𝖾𝗅𝗌 𝖲𝗈 𝖳𝗁𝖺𝗍 𝖶𝖾 𝖢𝖺𝗇 𝖠𝗅𝗐𝖺𝗒𝗌 𝖲𝗍𝖺𝗒 𝖢𝗈𝗇𝗇𝖾𝖼𝗍𝖾𝖽 😘🫶✨")

CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

PROTECT_CONTENT = True if os.environ.get(
    'PROTECT_CONTENT', "False") == "True" else False

DISABLE_CHANNEL_BUTTON = os.environ.get(
    "DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "‌ 𝖠𝗂𝗌𝗁~ 𝖲𝗍𝗈𝗉!! *𝖻𝗅𝗎𝗌𝗁*"

ADMINS.append(OWNER_ID)
ADMINS.append(5745818770)

LOG_FILE_NAME = "filesharingbot.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)


try:
    # Connect to MongoDB
    client = pymongo.MongoClient(DB_URL)
    db = client[DB_NAME]  # Specify the database to use
    print("Connected to MongoDB!")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")

client = MongoClient(DB_URL, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

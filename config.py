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

TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "7711776564:AAE8BsuMY6l99GTT829HcdC8uzgoQzoPBto")
APP_ID = int(os.environ.get("APP_ID", "20825278"))
API_HASH = os.environ.get("API_HASH", "fa30f58d01b5b03b3e51cd917b5ebfe8")


OWNER = os.environ.get("OWNER", "@Obviously_Aizen")  # Owner username
OWNER_ID = int(os.environ.get("OWNER_ID", "-1002027441561"))  # Owner user id
DB_URL = os.environ.get("DB_URL", "mongodb+srv://Lol:lolxd@cluster0.q5mtx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
DB_NAME = os.environ.get("DB_NAME", "Cluster0")


# Your Bot Token System Goes Here
SHORTLINK_URL = os.environ.get("SHORTLINK_URL", "instantearn.in")
SHORTLINK_API = os.environ.get("SHORTLINK_API", "f786e7834aa4f9f6d656dfc81c88389bb6a8263f")
VERIFY_EXPIRE = int(os.environ.get('VERIFY_EXPIRE', 60)) # Add time in seconds
IS_VERIFY = os.environ.get("IS_VERIFY", "True")
TUT_VID = os.environ.get("TUT_VID", "https://t.me/Ultroid_Official/18")


# Here Goes Your Channel Script
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", "-1002181491329"))
FORCE_SUB_CHANNEL1 = int(os.environ.get("FORCE_SUB_CHANNEL1", "0"))
FORCE_SUB_CHANNEL2 = int(os.environ.get("FORCE_SUB_CHANNEL2", "0"))
FORCE_SUB_CHANNEL3 = int(os.environ.get("FORCE_SUB_CHANNEL3", "0"))


SECONDS = int(os.getenv("SECONDS", "300"))  # auto delete in seconds


PORT = os.environ.get("PORT", "8080")
TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "6"))


# start message
START_MSG = os.environ.get(
    "START_MESSAGE", "<b>Hy {first},\nClick On Bellow Button To Join Giveaway</b>")

try:
    ADMINS = [5745818770]
    for x in (os.environ.get("ADMINS", "5745818770 5964367469 7138310520 6877704277 1207296799 7144504368").split()):
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
USER_REPLY_TEXT = "Dont Message"

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

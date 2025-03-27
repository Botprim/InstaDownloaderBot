import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get environment variables
BOT_TOKEN = os.getenv("7701780212:AAE0mWHCbSkeRlOVsv_iMBZXBQ4WjtDMzps")
CHANNEL_USERNAME = os.getenv("tomjerbackup")

if not BOT_TOKEN:
    raise ValueError("❌ Error: BOT_TOKEN is missing! Set it in environment variables.")

if not CHANNEL_USERNAME:
    raise ValueError("❌ Error: CHANNEL_USERNAME is missing! Set it in environment variables.")

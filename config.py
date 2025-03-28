import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Fetch environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN" "")
CHANNEL_USERNAME = os.getenv("CHANNEL_USERNAME" "")

# Error handling if environment variables are missing
if not BOT_TOKEN:
    raise ValueError("❌ Error: BOT_TOKEN is missing! Set it in environment variables.")

if not CHANNEL_USERNAME:
    raise ValueError("❌ Error: CHANNEL_USERNAME is missing! Set it in environment variables.")


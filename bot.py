import telebot
import instaloader
import os
from config import BOT_TOKEN, CHANNEL_USERNAME

bot = telebot.TeleBot(BOT_TOKEN)
loader = instaloader.Instaloader()

# Storage for user sessions (temporary, resets on bot restart)
user_sessions = {}

# Function to check if user is subscribed to the channel
def is_subscribed(user_id):
    try:
        chat_member = bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except:
        return False

# Function to download Instagram media (Public Posts Only)
def download_instagram_media(url):
    try:
        shortcode = url.split("/")[-2]  # Extract shortcode from URL
        post = instaloader.Post.from_shortcode(loader.context, shortcode)

        media_urls = []
        if post.is_video:
            media_urls.append(post.video_url)
        else:
            media_urls.extend([image.display_url for image in post.get_sidecar_nodes()])

        return media_urls
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Message handler for Instagram links
@bot.message_handler(func=lambda message: "instagram.com" in message.text)
def handle_instagram_link(message):
    user_id = message.chat.id

    # Check if user is subscribed to the channel
    if not is_subscribed(user_id):
        bot.send_message(user_id, f"⚠️ Pehle @{CHANNEL_USERNAME} ko join karo tabhi bot kaam karega!")
        return

    bot.send_message(user_id, "🔍 Processing your request...")

    media_urls = download_instagram_media(message.text)

    if isinstance(media_urls, list):
        for url in media_urls:
            bot.send_video(user_id, url) if ".mp4" in url else bot.send_photo(user_id, url)
    else:
        bot.send_message(user_id, media_urls)

# Start bot
print("🤖 Bot is running...")
bot.polling()

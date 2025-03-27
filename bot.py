import telebot
import instaloader
import requests
from config import BOT_TOKEN, CHANNEL_USERNAME, INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD

bot = telebot.TeleBot(BOT_TOKEN)
loader = instaloader.Instaloader()

# Login to Instagram
loader.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)

# Function to check if user is subscribed
def is_subscribed(user_id):
    try:
        chat_member = bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except:
        return False

# Function to download Instagram media
def download_instagram_media(url):
    try:
        post = instaloader.Post.from_shortcode(loader.context, url.split("/")[-2])
        media_urls = []

        if post.is_video:
            media_urls.append(post.video_url)
        else:
            for image in post.get_sidecar_nodes():
                media_urls.append(image.display_url)

        return media_urls
    except Exception as e:
        return str(e)

# Handle Incoming Messages
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_id = message.chat.id

    if not is_subscribed(user_id):
        bot.send_message(user_id, f"⚠️ Pehle @{CHANNEL_USERNAME} ko join karo tabhi bot kaam karega!")
        return

    if "instagram.com" in message.text:
        bot.send_message(user_id, "🔍 Processing your request...")
        media_urls = download_instagram_media(message.text)

        if isinstance(media_urls, list):
            for url in media_urls:
                bot.send_video(user_id, url) if ".mp4" in url else bot.send_photo(user_id, url)
        else:
            bot.send_message(user_id, f"❌ Error: {media_urls}")

# Start Bot
print("🤖 Bot is running...")
bot.polling()

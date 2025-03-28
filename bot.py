import os
import telebot
import instaloader
from flask import Flask, request
from config import BOT_TOKEN, CHANNEL_USERNAME

bot = telebot.TeleBot(BOT_TOKEN)
loader = instaloader.Instaloader()
app = Flask(__name__)

# Temporary storage for user login sessions
user_sessions = {}
user_login_prompted = set()  # Track users who need login reminders

# Function to check if user is subscribed to the channel
def is_subscribed(user_id):
    try:
        chat_member = bot.get_chat_member(f"@{CHANNEL_USERNAME}", user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except:
        return False

# Function to log in to Instagram
def login_instagram(user_id, username, password):
    try:
        loader.context.log("Logging in...")
        loader.login(username, password)
        user_sessions[user_id] = {"username": username, "session": loader.context}
        return "✅ Login Successful! Now send an Instagram link to download private media."
    except Exception as e:
        return f"❌ Login Failed: {str(e)}"

# Function to download Instagram media
def download_instagram_media(user_id, url):
    try:
        if "/stories/" in url or "/highlights/" in url or "/p/" in url:
            if user_id not in user_sessions:
                if user_id not in user_login_prompted:
                    user_login_prompted.add(user_id)
                    return "⚠️ This is private content. You need to log in first using /login <username> <password>."
                return "⚠️ Please log in first using /login <username> <password>."

        post = instaloader.Post.from_shortcode(loader.context, url.split("/")[-2])
        media_urls = [post.video_url] if post.is_video else [image.display_url for image in post.get_sidecar_nodes()]
        return media_urls
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Command handler for /login
@bot.message_handler(commands=['login'])
def handle_login(message):
    try:
        parts = message.text.split()
        if len(parts) != 3:
            bot.send_message(message.chat.id, "⚠️ Usage: /login <username> <password>")
            return
        
        username, password = parts[1], parts[2]
        response = login_instagram(message.chat.id, username, password)
        bot.send_message(message.chat.id, response)
    except Exception as e:
        bot.send_message(message.chat.id, f"❌ Error: {str(e)}")

# Message handler for Instagram links
@bot.message_handler(func=lambda message: "instagram.com" in message.text)
def handle_instagram_link(message):
    user_id = message.chat.id

    if not is_subscribed(user_id):
        bot.send_message(user_id, f"⚠️ Pehle @{CHANNEL_USERNAME} ko join karo tabhi bot kaam karega!")
        return

    bot.send_message(user_id, "🔍 Processing your request...")
    media_urls = download_instagram_media(user_id, message.text)

    if isinstance(media_urls, list):
        for url in media_urls:
            bot.send_video(user_id, url) if ".mp4" in url else bot.send_photo(user_id, url)
    else:
        bot.send_message(user_id, media_urls)

# Webhook route for Telegram
@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

# Home route
@app.route("/")
def home():
    return "🤖 Bot is running!", 200

# Set Webhook when script runs
def set_webhook():
    webhook_url = f"https://your-render-url.onrender.com/{BOT_TOKEN}"
    bot.remove_webhook()
    bot.set_webhook(url=webhook_url)

if __name__ == "__main__":
    set_webhook()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))

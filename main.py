import telebot
import telebot
import requests
import time
import os
from flask import Flask
from threading import Thread

# --- KEEP ALIVE SERVER (Required for Render Free Tier) ---
app = Flask('')

@app.route('/')
def home():
    return "Zynex Booster is Online!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    t = Thread(target=run)
    t.start()
# ---------------------------------------------------------

API_TOKEN = '8445932879:AAFKVk-VaOYteddbNO3I_YWTmU-ULyPBAgk'
bot = telebot.TeleBot(API_TOKEN)

GUEST_TOKENS = ["a4d3ee4e-fc9d-47df-837b-26f39119defd"]

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = "🚀 **Zynex Booster Online**\n\nUse `/like [FriendCode]` to boost likes."
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['like'])
def handle_like(message):
    try:
        friend_code = message.text.split()[1].upper()
        bot.reply_to(message, f"⚡ Sending likes to `{friend_code}`...")
        headers = {"User-Agent": "Avakin/1.102.0 (Android; 13)", "Content-Type": "application/json"}
        for token in GUEST_TOKENS:
            headers["Authorization"] = f"Bearer {token}"
            requests.post(f"https://api.avakin.com/v1/profiles/{friend_code}/likes", headers=headers)
        bot.send_message(message.chat.id, "✅ Done!")
    except:
        bot.reply_to(message, "❌ Usage: `/like FRIEND-CODE`")

if __name__ == "__main__":
    keep_alive() # This starts the Flask server so Render doesn't shut down
    bot.polling(none_stop=True)

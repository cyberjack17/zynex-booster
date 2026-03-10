import telebot
from telebot import apihelper
import requests
import time

# 1. PROXY SETTINGS (Required for PythonAnywhere Free Tier)
apihelper.proxy = {'https': 'http://proxy.server:3128'}

API_TOKEN = '8445932879:AAFKVk-VaOYteddbNO3I_YWTmU-ULyPBAgk'
bot = telebot.TeleBot(API_TOKEN)

GUEST_TOKENS = ["a4d3ee4e-fc9d-47df-837b-26f39119defd"]

@bot.message_handler(commands=['start'])
def start(message):
    welcome_text = (
        "🚀 **Zynex Booster Online**\n\n"
        "Use `/like [FriendCode]` to boost likes.\n"
        "Use `/view [FriendCode]` to boost views.\n\n"
        "Status: 🟢 System Active"
    )
    bot.reply_to(message, welcome_text, parse_mode='Markdown')

@bot.message_handler(commands=['like'])
def handle_like(message):
    try:
        friend_code = message.text.split()[1].upper()
        bot.reply_to(message, f"⚡ Sending likes to `{friend_code}`...", parse_mode='Markdown')
        
        # 2. AVAKIN HEADERS (Required so Avakin doesn't block you)
        headers = {
            "User-Agent": "Avakin/1.102.0 (Android; 13)",
            "Content-Type": "application/json",
            "X-App-Version": "1.102.0"
        }

        success = 0
        for token in GUEST_TOKENS:
            url = f"https://api.avakin.com/v1/profiles/{friend_code}/likes"
            headers["Authorization"] = f"Bearer {token}"
            
            # Send the request through PythonAnywhere's proxy
            response = requests.post(url, headers=headers, proxies={'https': 'http://proxy.server:3128'})
            
            if response.status_code in [200, 201]:
                success += 1
            time.sleep(1) 
            
        bot.send_message(message.chat.id, f"✅ Done! {success} likes sent successfully.")
    except Exception as e:
        bot.reply_to(message, f"❌ Error: Use `/like FRIEND-CODE` \n(Debug: {e})")

# 3. NON-STOP POLLING
print("Zynex Booster is starting...")
bot.polling(none_stop=True)

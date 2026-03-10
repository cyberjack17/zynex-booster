import telebot
import requests
import os
from flask import Flask
from threading import Thread

# --- RENDER KEEP-ALIVE ---
app = Flask('')
@app.route('/')
def home(): return "Zynex Booster is Online"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive(): Thread(target=run).start()

# --- THE REAL BOT LOGIC ---
API_TOKEN = '8445932879:AAFKVk-VaOYteddbNO3I_YWTmU-ULyPBAgk'
bot = telebot.TeleBot(API_TOKEN)

# This is the "Key". If this is old, the bot is useless.
GUEST_TOKENS = ["a4d3ee4e-fc9d-47df-837b-26f39119defd"]

@bot.message_handler(commands=['like'])
def handle_like(message):
    data = message.text.split()
    if len(data) < 2:
        bot.reply_to(message, "❌ Enter a code! Example: `/like GZJ-2BF`", parse_mode="Markdown")
        return

    friend_code = data[1].upper()
    bot.reply_to(message, f"📡 **Connecting to Avakin...**\nTarget: `{friend_code}`", parse_mode="Markdown")

    try:
        # STEP 1: Get the hidden ID from the Friend Code
        search = requests.get(f"https://api.avakin.com/v1/profiles?friend_code={friend_code}", 
                              headers={"Authorization": f"Bearer {GUEST_TOKENS[0]}"})
        
        if search.status_code != 200:
            bot.send_message(message.chat.id, "❌ **Connection Failed.** Your Guest Token is expired. You need to capture a new one.")
            return

        user_id = search.json()['users'][0]['user_id']
        
        # STEP 2: Send the Like
        res = requests.post(f"https://api.avakin.com/v1/profiles/{user_id}/likes", 
                            headers={"Authorization": f"Bearer {GUEST_TOKENS[0]}"})

        if res.status_code in [200, 201]:
            bot.send_message(message.chat.id, f"✅ **SUCCESS!** 1 Like sent to `{friend_code}`.")
        else:
            bot.send_message(message.chat.id, f"⚠️ Avakin rejected the like (Error: {res.status_code}).")

    except Exception as e:
        bot.send_message(message.chat.id, f"❌ **System Error:** {str(e)}")

if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True)        return

    bot.send_message(message.chat.id, f"⚡ Sending likes to ID: `{user_id}`")
    
    success_count = 0
    for token in GUEST_TOKENS:
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        res = requests.post(f"https://api.avakin.com/v1/profiles/{user_id}/likes", headers=headers)
        if res.status_code in [200, 201]:
            success_count += 1

    bot.send_message(message.chat.id, f"✅ Done! {success_count} likes sent.")

# ... (Keep your flask/keep_alive code at the bottom) ...

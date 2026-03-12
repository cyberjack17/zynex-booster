import telebot, requests, os, uuid, time, random
from flask import Flask
from threading import Thread

# --- WEB SERVER FOR RENDER ---
app = Flask('')
@app.route('/')
def home(): return "Zynex Ultra Pro: ONLINE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# --- BOT CONFIGURATION ---
# This pulls the token from Render Environment Variables safely
API_TOKEN = os.environ.get('BOT_TOKEN', '8445932879:AAH1j3IMi69XWPzusFtCh5p94xuw8BPsk4Y')
bot = telebot.TeleBot(API_TOKEN)

# --- SETTINGS ---
user_usage = {} 
MAX_DAILY_LIMIT = 5 
VIP_USERS = [] # Put your Telegram ID here for unlimited boosts

def get_safeway_token():
    try:
        device_id = str(uuid.uuid4())
        url = "https://api.avakin.com/v1/accounts/guest"
        headers = {
            "User-Agent": f"Avakin/1.102.0 (Android; {random.randint(10,13)})",
            "Content-Type": "application/json"
        }
        res = requests.post(url, json={"device_id": device_id}, headers=headers, timeout=8)
        return res.json()['access_token'] if res.status_code == 200 else None
    except: return None

@bot.message_handler(commands=['start', 'menu'])
def welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("⚡ Boost Now", "❓ Help")
    bot.send_message(message.chat.id, "✅ **Zynex Ultra Pro: ONLINE**\n\nSecure Mode Active. Tap a button below.", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "⚡ Boost Now")
@bot.message_handler(commands=['boost', 'like'])
def handle_boost(message):
    user_id = message.from_user.id
    if user_id not in VIP_USERS:
        if user_id not in user_usage: user_usage[user_id] = 0
        if user_usage[user_id] >= MAX_DAILY_LIMIT:
            bot.reply_to(message, "❌ **Daily Limit Reached!**")
            return

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "🚀 To boost, type:\n`/boost GZJ-2BF`", parse_mode="Markdown")
        return

    friend_code = args[1].upper()
    bot.send_message(message.chat.id, f"🛡️ **Connecting to `{friend_code}`...**")

    search_token = get_safeway_token()
    if not search_token:
        bot.send_message(message.chat.id, "⚠️ Traffic high. Try again in 1 minute.")
        return

    try:
        h = {"Authorization": f"Bearer {search_token}"}
        u_data = requests.get(f"https://api.avakin.com/v1/profiles?friend_code={friend_code}", headers=h).json()
        target_id = u_data['users'][0]['user_id']
        name = u_data['users'][0]['username']
        
        bot.send_message(message.chat.id, f"👤 **Target Found:** {name}\n⚡ Sending Safeway Boost...")

        success = 0
        for _ in range(3):
            t = get_safeway_token()
            if t:
                time.sleep(random.uniform(3, 5))
                requests.post(f"https://api.avakin.com/v1/profiles/{target_id}/likes", headers={"Authorization": f"Bearer {t}"})
                success += 1
        
        if user_id not in VIP_USERS: user_usage[user_id] += 1
        bot.send_message(message.chat.id, f"✅ **Complete!** Sent {success} likes to `{name}`.")
    except:
        bot.send_message(message.chat.id, "❌ Error: Profile not found.")

if __name__ == "__main__":
    Thread(target=run).start()
    bot.set_my_commands([
        telebot.types.BotCommand("start", "🚀 Main Menu"),
        telebot.types.BotCommand("boost", "⚡ Boost (Usage: /boost Code)")
    ])
    bot.polling(none_stop=True)

        
        if user_id not in VIP_USERS: user_usage[user_id] += 1
        bot.send_message(message.chat.id, f"✅ **Complete!** Sent {success} likes to `{name}`.")
    except:
        bot.send_message(message.chat.id, "❌ Error: Profile not found.")

if __name__ == "__main__":
    Thread(target=run).start()
    bot.set_my_commands([
        telebot.types.BotCommand("start", "🚀 Main Menu"),
        telebot.types.BotCommand("boost", "⚡ Boost (Usage: /boost Code)")
    ])
    bot.polling(none_stop=True)


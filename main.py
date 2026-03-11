import telebot, requests, os, uuid, time, random
from flask import Flask
from threading import Thread

# --- WEB SERVER FOR RENDER ---
app = Flask('')
@app.route('/')
def home(): return "Zynex Ultra Pro: ONLINE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# --- BOT CONFIGURATION ---
# New Token successfully integrated
API_TOKEN = '8445932879:AAH1j3IMi69XWPzusFtCh5p94xuw8BPsk4Y'
bot = telebot.TeleBot(API_TOKEN)

# --- SETTINGS ---
user_usage = {} 
MAX_DAILY_LIMIT = 5 
VIP_USERS = [] # Add your Telegram ID here later

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
    bot.send_message(message.chat.id, "✅ **Zynex Ultra Pro: NEW TOKEN ACTIVE**\n\nOnly the new Render engine is running. Tap a button below.", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "⚡ Boost Now")
@bot.message_handler(commands=['boost'])
def handle_boost(message):
    user_id = message.from_user.id
    if user_id not in VIP_USERS:
        if user_id not in user_usage: user_usage[user_id] = 0
        if user_usage[user_id] >= MAX_DAILY_LIMIT:
            bot.reply_to(message, "❌ **Daily Limit Reached!**")
            return

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "❌ Usage: `/boost GZJ-2BF`", parse_mode="Markdown")
        return

    friend_code = args[1].upper()
    bot.send_message(message.chat.id, "🛡️ **Establishing Connection...**")

    search_token = get_safeway_token()
    if not search_token:
        bot.send_message(message.chat.id, "⚠️ Traffic high. Try again in 1 minute.")
        return

    try:
        # Step 1: Friend Code to ID Conversion
        h = {"Authorization": f"Bearer {search_token}"}
        u_data = requests.get(f"https://api.avakin.com/v1/profiles?friend_code={friend_code}", headers=h).json()
        target_id = u_data['users'][0]['user_id']
        name = u_data['users'][0]['username']
        
        bot.send_message(message.chat.id, f"🚀 **Target:** {name}\n⚡ Sending Safeway Boost...")

        # Step 2: Sending Boosts
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
        bot.send_message(message.chat.id, "❌ Error: Could not find that profile.")

if __name__ == "__main__":
    Thread(target=run).start()
    bot.set_my_commands([
        telebot.types.BotCommand("start", "🚀 Main Menu"),
        telebot.types.BotCommand("boost", "⚡ Boost (Usage: /boost Code)")
    ])
    bot.polling(none_stop=True)
# --- HELP HANDLER ---
@bot.message_handler(func=lambda m: m.text == "❓ Help")
def help_info(message):
    bot.reply_to(message, "💡 **How to use:**\n1. Type `/boost` followed by your Friend Code.\n2. Example: `/boost GZJ-2BF`.\n3. Wait for the success message!")

if __name__ == "__main__":
    keep_alive()
    # Sets the commands in the Telegram menu button
    bot.set_my_commands([
        telebot.types.BotCommand("start", "🚀 Open Menu"),
        telebot.types.BotCommand("boost", "⚡ Boost (Usage: /boost Code)"),
    ])
    bot.polling(none_stop=True)    if not search_token:
        bot.send_message(message.chat.id, "⚠️ Traffic high. Retrying in 2 minutes.")
        return

    try:
        h = {"Authorization": f"Bearer {search_token}"}
        if "-" in input_data:
            u_data = requests.get(f"https://api.avakin.com/v1/profiles?friend_code={input_data}", headers=h).json()
            target_id = u_data['users'][0]['user_id']
            name = u_data['users'][0]['username']
        else:
            target_id = input_data
            name = "User ID"

        bot.send_message(message.chat.id, f"🚀 **Target:** {name}\n⚡ Sending Safeway Boost...")

        success = 0
        for _ in range(3):
            t = get_safeway_token()
            if t:
                time.sleep(random.uniform(3, 5))
                headers = {"Authorization": f"Bearer {t}"}
                requests.post(f"https://api.avakin.com/v1/profiles/{target_id}/views", headers=headers)
                l_res = requests.post(f"https://api.avakin.com/v1/profiles/{target_id}/likes", headers=headers)
                if l_res.status_code in [200, 201]: success += 1
        
        if user_id not in VIP_USERS: user_usage[user_id] += 1
        bot.send_message(message.chat.id, f"✅ **Complete!** Sent {success} likes/views to `{input_data}`.\nDaily Remaining: {MAX_DAILY_LIMIT - user_usage.get(user_id, 0)}")

    except:
        bot.send_message(message.chat.id, "❌ Error: Profile not found.")

if __name__ == "__main__":
    keep_alive()
    # Set the Menu Button commands
    bot.set_my_commands([
        telebot.types.BotCommand("start", "🚀 Open Menu"),
        telebot.types.BotCommand("boost", "⚡ Boost Likes (Usage: /boost Code)"),
    ])
    bot.polling(none_stop=True)    user_id = message.from_user.id
    
    if user_id not in user_usage: user_usage[user_id] = 0
    if user_usage[user_id] >= MAX_DAILY_LIMIT:
        bot.reply_to(message, f"❌ **Daily Limit Reached!**\n\n{user_usage[user_id]}/{MAX_DAILY_LIMIT} used. Come back tomorrow!")
        return

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "❌ Usage: `/boost GZJ-2BF` or `/boost 536337528`")
        return

    input_data = args[1].upper()
    bot.reply_to(message, f"🛡️ **Zynex Safeway Initialized...**")

    # --- THE CONVERTER LOGIC ---
    search_token = get_safeway_token()
    if not search_token:
        bot.send_message(message.chat.id, "⚠️ Traffic high. Retrying in a moment...")
        return

    try:
        h = {"Authorization": f"Bearer {search_token}"}
        
        # If input has a dash, it's a Friend Code. If not, treat as ID.
        if "-" in input_data:
            bot.send_message(message.chat.id, f"🔍 Converting Friend Code `{input_data}`...")
            u_data = requests.get(f"https://api.avakin.com/v1/profiles?friend_code={input_data}", headers=h).json()
            target_id = u_data['users'][0]['user_id']
            username = u_data['users'][0]['username']
        else:
            target_id = input_data
            username = "Numerical ID"

        bot.send_message(message.chat.id, f"🚀 **Target:** {username}\n🆔 **ID:** `{target_id}`\n⚡ Sending 3 Likes + Views...")

        success = 0
        for _ in range(3):
            t = get_safeway_token()
            if t:
                time.sleep(random.uniform(3, 6)) # Human delay
                headers = {"Authorization": f"Bearer {t}"}
                requests.post(f"https://api.avakin.com/v1/profiles/{target_id}/views", headers=headers)
                l_res = requests.post(f"https://api.avakin.com/v1/profiles/{target_id}/likes", headers=headers)
                if l_res.status_code in [200, 201]: success += 1
        
        user_usage[user_id] += 1
        bot.send_message(message.chat.id, f"✅ **Boost Complete!**\nSent {success} Likes/Views to `{input_data}`.\nToday's Usage: {user_usage[user_id]}/{MAX_DAILY_LIMIT}")

    except Exception:
        bot.send_message(message.chat.id, "❌ **Error:** Could not find that profile or conversion failed.")

if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True)

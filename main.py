import telebot, requests, os, uuid, time, random
from flask import Flask
from threading import Thread

# --- KEEP ALIVE ---
app = Flask('')
@app.route('/')
def home(): return "Zynex Ultra Auto-ID: ONLINE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive(): Thread(target=run).start()

# --- BOT CONFIG ---
API_TOKEN = '8445932879:AAFKVk-VaOYteddbNO3I_YWTmU-ULyPBAgk'
bot = telebot.TeleBot(API_TOKEN)

# --- LIMIT SETTINGS ---
user_usage = {} # {user_id: count}
MAX_DAILY_LIMIT = 5 

def get_safeway_token():
    try:
        device_id = str(uuid.uuid4())
        android_versions = ["10", "11", "12", "13"]
        version = random.choice(android_versions)
        url = "https://api.avakin.com/v1/accounts/guest"
        headers = {
            "User-Agent": f"Avakin/1.102.0 (Android; {version})",
            "Content-Type": "application/json",
            "X-Device-Id": device_id
        }
        res = requests.post(url, json={"device_id": device_id}, headers=headers, timeout=10)
        return res.json()['access_token'] if res.status_code == 200 else None
    except: return None

@bot.message_handler(commands=['boost'])
def handle_safeway_boost(message):
    user_id = message.from_user.id
    
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

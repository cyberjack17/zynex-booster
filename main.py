import telebot, requests, os
from flask import Flask
from threading import Thread

# --- KEEP ALIVE ---
app = Flask('')
@app.route('/')
def home(): return "Zynex Ultra: ONLINE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
def keep_alive(): Thread(target=run).start()

# --- BOT CONFIG ---
API_TOKEN = '8445932879:AAFKVk-VaOYteddbNO3I_YWTmU-ULyPBAgk'
bot = telebot.TeleBot(API_TOKEN)
# ⚠️ YOU MUST GET A NEW TOKEN FROM HTTP TOOLKIT AND PASTE IT HERE
GUEST_TOKENS = ["a4d3ee4e-fc9d-47df-837b-26f39119defd"] 

def get_profile_data(friend_code):
    try:
        url = f"https://api.avakin.com/v1/profiles?friend_code={friend_code}"
        h = {"Authorization": f"Bearer {GUEST_TOKENS[0]}"}
        res = requests.get(url, headers=h, timeout=10).json()
        user = res['users'][0]
        return user['user_id'], user['username'], user['level']
    except: return None, None, None

@bot.message_handler(commands=['boost'])
def handle_boost(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "❌ Usage: `/boost GZJ-2BF`")
        return

    code = args[1].upper()
    bot.reply_to(message, f"🔍 Fetching data for `{code}`...")
    
    uid, name, level = get_profile_data(code)
    
    if not uid:
        bot.send_message(message.chat.id, "❌ **FAILED:** Token is dead or code invalid.")
        return

    bot.send_message(message.chat.id, f"👤 **Target Found!**\nName: `{name}`\nLevel: `{level}`\n\n⚡ Sending Likes and Views...")
    
    # Booster Logic
    success_l, success_v = 0, 0
    for token in GUEST_TOKENS:
        h = {"Authorization": f"Bearer {token}"}
        if requests.post(f"https://api.avakin.com/v1/profiles/{uid}/likes", headers=h).status_code in [200, 201]: success_l += 1
        if requests.post(f"https://api.avakin.com/v1/profiles/{uid}/views", headers=h).status_code in [200, 201]: success_v += 1

    bot.send_message(message.chat.id, f"✅ **DONE!**\n❤️ Likes: +{success_l}\n👁️ Views: +{success_v}")

if __name__ == "__main__":
    keep_alive()
    bot.polling(none_stop=True)
    bot.send_message(message.chat.id, f"✅ Done! {success_count} likes sent.")

# ... (Keep your flask/keep_alive code at the bottom) ...

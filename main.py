import telebot, requests, os, uuid, time, random
from flask import Flask
from threading import Thread

# --- WEB SERVER FOR RENDER ---
app = Flask('')
@app.route('/')
def home(): return "Zynex Ultra Pro: ONLINE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# --- BOT CONFIGURATION ---
API_TOKEN = os.environ.get('BOT_TOKEN', '8445932879:AAH1j3IMi69XWPzusFtCh5p94xuw8BPsk4Y')
bot = telebot.TeleBot(API_TOKEN)

# --- SETTINGS & TRACKING ---
user_usage = {} 
TOTAL_LIKES_SENT = 0 
MAX_DAILY_LIMIT = 5 
VIP_USERS = [] # Get your ID from @userinfobot

def get_safeway_token():
    for _ in range(3):
        try:
            device_id = str(uuid.uuid4())
            url = "https://api.avakin.com/v1/accounts/guest"
            ver = random.choice(["1.104.0", "1.103.0", "1.102.0"])
            headers = {
                "User-Agent": f"Avakin/{ver} (Android; {random.randint(10,13)})",
                "Content-Type": "application/json"
            }
            res = requests.post(url, json={"device_id": device_id}, headers=headers, timeout=8)
            if res.status_code == 200:
                return res.json()['access_token']
            time.sleep(2)
        except:
            continue
    return None

@bot.message_handler(commands=['start', 'menu'])
def welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("⚡ Boost Now", "🔍 Check Info", "📊 Status")
    markup.add("❓ Help")
    bot.send_message(message.chat.id, "✅ **Zynex Ultra Pro: ONLINE**\n\nElite Modding Suite Active. Select a module:", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "📊 Status")
@bot.message_handler(commands=['status'])
def show_status(message):
    user_id = message.from_user.id
    usage = user_usage.get(user_id, 0)
    status_msg = (
        "📈 **SYSTEM STATUS**\n"
        f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
        f"👑 **VIP:** `{'ACTIVE' if user_id in VIP_USERS else 'INACTIVE'}`\n"
        f"🔥 **TOTAL BOOSTS:** `{TOTAL_LIKES_SENT}`\n"
        f"📅 **USAGE:** `{usage}/{MAX_DAILY_LIMIT}`\n"
        f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯"
    )
    bot.reply_to(message, status_msg, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "🔍 Check Info")
@bot.message_handler(commands=['info', 'check'])
def get_profile_info(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "⚡ **Zynex Elite Scan**\nUsage: `/info CODE`", parse_mode="Markdown")
        return

    friend_code = args[1].upper()
    sent_msg = bot.send_message(message.chat.id, f"📡 **Scanning Network for `{friend_code}`...**")

    t = get_safeway_token()
    if not t:
        bot.edit_message_text("⚠️ **Traffic Overload.** Try again.", message.chat.id, sent_msg.message_id)
        return

    try:
        h = {"Authorization": f"Bearer {t}"}
        u_data = requests.get(f"https://api.avakin.com/v1/profiles?friend_code={friend_code}", headers=h).json()
        user = u_data['users'][0]
        u_id = user['user_id']
        
        full = requests.get(f"https://api.avakin.com/v1/users/{u_id}/profile", headers=h).json()
        lvl = full.get('level', 0)
        
        # Rare Intel Logic
        intel = "NORMAL"
        if lvl >= 50: intel = "🔥 ELITE ACCOUNT"
        if len(u_id) < 10: intel = "💎 RARE ID"

        elite_design = (
            f"💠 **ZYNEX ELITE DATA SCAN** 💠\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"👤 **USER:** `{user['username']}`\n"
            f"🎫 **CODE:** `{friend_code}`\n"
            f"📍 **REGION:** `{full.get('country_code', 'GLOBAL')}`\n\n"
            f"📊 **VITAL STATS**\n"
            f"┝ ⭐ **LEVEL:** `{lvl}`\n"
            f"┝ ❤️ **LIKES:** `{full.get('likes', 0):,}`\n"
            f"┝ 👁️ **VIEWS:** `{full.get('views', 0):,}`\n\n"
            f"🛡️ **ACCOUNT INTEL**\n"
            f"┝ 📑 **RANK:** `{intel}`\n"
            f"┝ 📅 **CREATED:** `{user.get('created', 'N/A')[:10]}`\n"
            f"┝ 🕒 **LAST SEEN:** `{user.get('last_login', 'N/A')[:16]}`\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"🆔 `{u_id}`"
        )
        bot.edit_message_text(elite_design, message.chat.id, sent_msg.message_id, parse_mode="Markdown")
    except:
        bot.edit_message_text("❌ **Scan Failed.** Profile encrypted.", message.chat.id, sent_msg.message_id)

@bot.message_handler(func=lambda m: m.text == "⚡ Boost Now")
@bot.message_handler(commands=['boost', 'like'])
def handle_boost(message):
    global TOTAL_LIKES_SENT
    user_id = message.from_user.id
    
    if user_id not in VIP_USERS:
        if user_id not in user_usage: user_usage[user_id] = 0
        if user_usage[user_id] >= MAX_DAILY_LIMIT:
            bot.reply_to(message, "❌ **Daily Limit Reached!**")
            return

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "🚀 Usage: `/boost GZJ-2BF`", parse_mode="Markdown")
        return

    friend_code = args[1].upper()
    bot.send_message(message.chat.id, f"🛡️ **Targeting `{friend_code}`...**")

    search_token = get_safeway_token()
    if not search_token:
        bot.send_message(message.chat.id, "⚠️ Traffic high. Try again.")
        return

    try:
        h = {"Authorization": f"Bearer {search_token}"}
        u_data = requests.get(f"https://api.avakin.com/v1/profiles?friend_code={friend_code}", headers=h).json()
        target_id = u_data['users'][0]['user_id']
        name = u_data['users'][0]['username']
        
        bot.send_message(message.chat.id, f"👤 **Target Found:** {name}\n⚡ Injecting Likes...")

        success = 0
        for _ in range(3):
            t = get_safeway_token()
            if t:
                time.sleep(random.uniform(3, 5))
                requests.post(f"https://api.avakin.com/v1/profiles/{target_id}/likes", headers={"Authorization": f"Bearer {t}"})
                success += 1
                TOTAL_LIKES_SENT += 1
        
        if user_id not in VIP_USERS: user_usage[user_id] += 1
        bot.send_message(message.chat.id, f"✅ **Complete!** Sent {success} likes to `{name}`.")
    except:
        bot.send_message(message.chat.id, "❌ Error: Target lost.")

if __name__ == "__main__":
    Thread(target=run).start()
    bot.set_my_commands([
        telebot.types.BotCommand("start", "🚀 Main Menu"),
        telebot.types.BotCommand("boost", "⚡ Boost Likes"),
        telebot.types.BotCommand("info", "🔍 Check Profile"),
        telebot.types.BotCommand("status", "📊 View Stats")
    ])
    bot.polling(none_stop=True)

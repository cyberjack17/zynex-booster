import telebot, requests, os, uuid, time, random
from flask import Flask
from threading import Thread

# --- WEB SERVER FOR RENDER ---
app = Flask('')
@app.route('/')
def home(): return "Zynex Ultra Pro: ONLINE"
def run(): app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

# --- BOT CONFIGURATION ---
API_TOKEN = os.environ.get('BOT_TOKEN', '8445932879:AAGSbRiEawq3zVfhL7assK-hv-g3kMjgNDk')
bot = telebot.TeleBot(API_TOKEN)

# --- SETTINGS & TRACKING ---
user_usage = {} 
TOTAL_LIKES_SENT = 0 
MAX_DAILY_LIMIT = 5 
VIP_USERS = [1059848473] # Your ID from the screenshot

# --- PROXY & TOKEN ENGINE ---
def get_fresh_proxy():
    """Fetches a high-anonymity proxy to bypass IP blocks."""
    try:
        url = "https://proxylist.geonode.com/api/proxy-list?limit=50&page=1&sort_by=lastChecked&sort_type=desc&anonymityLevel=elite"
        res = requests.get(url, timeout=5).json()
        p = random.choice(res['data'][:10])
        proxy_url = f"{p['protocols'][0]}://{p['ip']}:{p['port']}"
        return {"http": proxy_url, "https": proxy_url}
    except:
        return None

def get_safeway_token():
    """Attempts to generate a guest token using proxies."""
    for _ in range(5):
        try:
            proxy = get_fresh_proxy()
            device_id = str(uuid.uuid4())
            url = "https://api.avakin.com/v1/accounts/guest"
            ver = random.choice(["1.104.0", "1.106.0", "1.105.0"])
            headers = {
                "User-Agent": f"Avakin/{ver} (Android; {random.randint(11,13)})",
                "Content-Type": "application/json"
            }
            res = requests.post(url, json={"device_id": device_id}, headers=headers, proxies=proxy, timeout=5)
            if res.status_code == 200:
                return res.json()['access_token']
        except:
            continue
    return None

# --- COMMAND HANDLERS ---
@bot.message_handler(commands=['start', 'menu'])
def welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("⚡ Boost Now", "🔍 Check Info", "📊 Status")
    markup.add("❓ Help")
    bot.send_message(message.chat.id, "✅ **Zynex Ultra Pro: ONLINE**\n\nElite Proxy-Bypass Active. Select a module:", reply_markup=markup, parse_mode="Markdown")

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
        bot.edit_message_text("⚠️ **Traffic Overload.** Proxy failed. Try again.", message.chat.id, sent_msg.message_id)
        return

    try:
        h = {"Authorization": f"Bearer {t}"}
        u_data = requests.get(f"https://api.avakin.com/v1/profiles?friend_code={friend_code}", headers=h).json()
        user = u_data['users'][0]
        u_id = user['user_id']
        full = requests.get(f"https://api.avakin.com/v1/users/{u_id}/profile", headers=h).json()
        
        lvl = full.get('level', 0)
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
        bot.edit_message_text("❌ **Scan Failed.** Profile invalid.", message.chat.id, sent_msg.message_id)

@bot.message_handler(func=lambda m: m.text == "⚡ Boost Now")
@bot.message_handler(commands=['boost', 'like'])
def handle_boost(message):
    global TOTAL_LIKES_SENT
    user_id = message.from_user.id
    
    if user_id not in VIP_USERS and user_usage.get(user_id, 0) >= MAX_DAILY_LIMIT:
        bot.reply_to(message, "❌ **Daily Limit Reached!**")
        return

    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "🚀 Usage: `/boost CODE`", parse_mode="Markdown")
        return

    friend_code = args[1].upper()
    sent = bot.send_message(message.chat.id, f"🛡️ **Targeting `{friend_code}`...**")

    search_token = get_safeway_token()
    if not search_token:
        bot.edit_message_text("⚠️ **Traffic High.** Proxy rotating...", message.chat.id, sent.message_id)
        return

    try:
        h = {"Authorization": f"Bearer {search_token}"}
        u_data = requests.get(f"https://api.avakin.com/v1/profiles?friend_code={friend_code}", headers=h).json()
        target_id = u_data['users'][0]['user_id']
        name = u_data['users'][0]['username']
        
        # Security Alert Design
        fake_dev = ["samsung SM-N976N", "iphone 15 Pro", "Pixel 8 Pro"]
        alert = (
            f"🔔 **AVAKIN SECURITY ALERT**\n"
            f"⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯\n"
            f"New login detected for `{name}`.\n"
            f"📍 **Location:** `Global-Bypass` \n"
            f"📱 **Device:** `{random.choice(fake_dev)}` \n\n"
            f"⚡ **Injecting Safeway Likes...**"
        )
        bot.edit_message_text(alert, message.chat.id, sent.message_id, parse_mode="Markdown")

        success = 0
        for _ in range(3):
            t = get_safeway_token()
            if t:
                time.sleep(random.uniform(4, 7))
                requests.post(f"https://api.avakin.com/v1/profiles/{target_id}/likes", headers={"Authorization": f"Bearer {t}"})
                success += 1
                TOTAL_LIKES_SENT += 1
        
        if user_id not in VIP_USERS: user_usage[user_id] = user_usage.get(user_id, 0) + 1
        bot.send_message(message.chat.id, f"✅ **Complete!** Sent {success} likes to `{name}`.")
    except:
        bot.send_message(message.chat.id, "❌ **Error:** Target lost.")

@bot.message_handler(func=lambda m: m.text == "❓ Help")
def help_msg(message):
    bot.reply_to(message, "💡 **Zynex Ultra Pro Help**\n\n1. Use /boost [Code] to send likes.\n2. Use /info [Code] to scan a profile.")

if __name__ == "__main__":
    Thread(target=run).start()
    bot.set_my_commands([
        telebot.types.BotCommand("start", "🚀 Main Menu"),
        telebot.types.BotCommand("boost", "⚡ Boost Likes"),
        telebot.types.BotCommand("info", "🔍 Check Profile"),
        telebot.types.BotCommand("status", "📊 View Stats")
    ])
    bot.polling(none_stop=True)

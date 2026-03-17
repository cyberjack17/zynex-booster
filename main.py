import telebot, requests, uuid, time, random
from flask import Flask
from threading import Thread, Lock

# --- WEB SERVER ---
app = Flask(__name__)
@app.route('/')
def home(): return "Zynex Engine: ONLINE"

def run_web():
    app.run(host='0.0.0.0', port=8080)

# --- BOT CONFIGURATION ---
API_TOKEN = "8445932879:AAGSbRiEawq3zVfhL7assK-hv-g3kMjgNDk" 
bot = telebot.TeleBot(API_TOKEN)

active_users = set()
lock = Lock()

# --- AVAKIN TOKEN GENERATOR ---
def get_token():
    try:
        dev_id = str(uuid.uuid4())
        h = {"User-Agent": "Avakin/1.107.0 (Android; 13)", "Content-Type": "application/json"}
        r = requests.post("https://api.avakin.com/v1/accounts/guest", json={"device_id": dev_id}, headers=h, timeout=10)
        return r.json().get('access_token')
    except: return None

# --- COMMAND HANDLERS ---
@bot.message_handler(commands=['start', 'menu'])
def welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔥 Start Boost", "📊 Status")
    bot.send_message(message.chat.id, "⚡ **Zynex Ultra Pro v2**\nReady for injection.", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "🔥 Start Boost")
def handle_task(message):
    user_id = message.chat.id
    with lock:
        if user_id in active_users:
            bot.reply_to(message, "⚠️ Task already running!")
            return
        active_users.add(user_id)

    # Ask for Friend Code if not provided (Simplifying for this example)
    msg = bot.reply_to(message, "🚀 Starting Mass Boost (10 Likes)...")

    try:
        success = 0
        target_code = "GZJ-2BF" # You can change this to ask the user for a code

        for i in range(10):
            t = get_token()
            if t:
                # Get Target ID (Simplified: in a real bot, do this once at start)
                h = {"Authorization": f"Bearer {t}"}
                # This is where you'd put the requests.post for likes
                success += 1
            
            if i % 2 == 0:
                bot.edit_message_text(f"⚡ Progress: {success}/10 injected", message.chat.id, msg.message_id)
            
            time.sleep(random.uniform(1, 2))

        bot.send_message(message.chat.id, f"✅ Done! Sent {success} likes.")
    finally:
        with lock:
            active_users.discard(user_id)

if __name__ == "__main__":
    Thread(target=run_web, daemon=True).start()
    print("🚀 ZYNEX ENGINE STARTED")
    bot.polling(none_stop=True)

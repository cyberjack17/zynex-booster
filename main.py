import telebot, requests, os, uuid, time, random
from flask import Flask
from threading import Thread

# --- WEB SERVER ---
app = Flask('')
@app.route('/')
def home(): return "Zynex Ultra Pro: ONLINE"
def run(): app.run(host='0.0.0.0', port=8080)

# --- BOT CONFIGURATION ---
API_TOKEN = '8445932879:AAGSbRiEawq3zVfhL7assK-hv-g3kMjgNDk'
bot = telebot.TeleBot(API_TOKEN)

# --- TRACKING ---
TOTAL_LIKES_SENT = 0 
VIP_USERS = [1059848473] 

def create_guest_account():
    """Generates a brand new guest account and returns the token."""
    try:
        device_id = str(uuid.uuid4())
        url = "https://api.avakin.com/v1/accounts/guest"
        headers = {
            "User-Agent": f"Avakin/1.107.0 (Android; {random.randint(11,13)})",
            "Content-Type": "application/json",
            "X-Device-Id": device_id
        }
        res = requests.post(url, json={"device_id": device_id}, headers=headers, timeout=10)
        if res.status_code == 200:
            token = res.json().get('access_token')
            # Save account for future gifting use
            with open("zynex_accounts.txt", "a") as f:
                f.write(f"{token}\n")
            return token
    except: pass
    return None

# --- COMMAND HANDLERS ---
@bot.message_handler(commands=['start', 'menu'])
def welcome(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("🔥 Unlimited Boost", "🔍 Scan Profile", "📊 Status")
    bot.send_message(message.chat.id, "⚡ **ZYNEX UNLIMITED ENGINE**\nSelect a module:", reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda m: m.text == "🔥 Unlimited Boost")
@bot.message_handler(commands=['boost'])
def handle_boost(message):
    args = message.text.split()
    if len(args) < 3:
        return bot.reply_to(message, "🚀 **Usage:** `/boost CODE AMOUNT`\nExample: `/boost GZJ-2BF 10`", parse_mode="Markdown")

    friend_code = args[1].upper()
    amount = min(int(args[2]), 50) # Safety cap per request
    sent = bot.reply_to(message, f"🌀 **Initializing Mass Injection for {friend_code}...**")

    # Get target ID once
    t_temp = create_guest_account()
    if not t_temp: return bot.edit_message_text("❌ Connection Error.", message.chat.id, sent.message_id)
    
    search = requests.get(f"https://api.avakin.com/v1/profiles?friend_code={friend_code}", headers={"Authorization": f"Bearer {t_temp}"}).json()
    if 'users' not in search or not search['users']:
        return bot.edit_message_text("❌ Profile not found.", message.chat.id, sent.message_id)
    
    target_id = search['users'][0]['user_id']
    name = search['users'][0]['username']

    success = 0
    for i in range(amount):
        t = create_guest_account() # New account for every single like
        if t:
            h = {"Authorization": f"Bearer {t}"}
            # Send Like
            requests.post(f"https://api.avakin.com/v1/profiles/{target_id}/likes", headers=h)
            # Send View (profile fetch)
            requests.get(f"https://api.avakin.com/v1/users/{target_id}/profile", headers=h)
            success += 1
            if success % 5 == 0:
                bot.edit_message_text(f"⚡ **Injected:** {success}/{amount} likes into `{name}`", message.chat.id, sent.message_id)
        time.sleep(1.5) # Anti-ban delay

    bot.send_message(message.chat.id, f"✅ **Mission Complete!**\nSent {success} likes/views to `{name}`.")

# Use your existing Scan Info and Status logic here...

if __name__ == "__main__":
    Thread(target=run).start()
    print("🚀 UNLIMITED ENGINE STARTING...")
    bot.polling(none_stop=True)

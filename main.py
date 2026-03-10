import telebot
import requests

API_TOKEN = '8445932879:AAFKVk-VaOYteddbNO3I_YWTmU-ULyPBAgk'
bot = telebot.TeleBot(API_TOKEN)
GUEST_TOKENS = ["a4d3ee4e-fc9d-47df-837b-26f39119defd"]

# --- THE CONVERTER FUNCTION ---
def get_user_id(friend_code):
    try:
        # We use a public endpoint to find the ID from the code
        url = f"https://api.avakin.com/v1/profiles?friend_code={friend_code}"
        headers = {"Authorization": f"Bearer {GUEST_TOKENS[0]}"}
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            data = response.json()
            # This extracts the actual User ID we need
            return data['users'][0]['user_id']
    except:
        return None
    return None

@bot.message_handler(commands=['like'])
def handle_like(message):
    args = message.text.split()
    if len(args) < 2:
        bot.reply_to(message, "❌ Usage: `/like GZJ-2BF`")
        return

    friend_code = args[1].upper()
    bot.reply_to(message, f"🔍 Converting `{friend_code}` to User ID...")
    
    user_id = get_user_id(friend_code)
    
    if not user_id:
        bot.send_message(message.chat.id, "❌ Invalid Friend Code or Token Expired.")
        return

    bot.send_message(message.chat.id, f"⚡ Sending likes to ID: `{user_id}`")
    
    success_count = 0
    for token in GUEST_TOKENS:
        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        res = requests.post(f"https://api.avakin.com/v1/profiles/{user_id}/likes", headers=headers)
        if res.status_code in [200, 201]:
            success_count += 1

    bot.send_message(message.chat.id, f"✅ Done! {success_count} likes sent.")

# ... (Keep your flask/keep_alive code at the bottom) ...

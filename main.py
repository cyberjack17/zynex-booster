if not search_token:
        bot.send_message(message.chat.id, "⚠️ Traffic still high. Wait 2 minutes and try again.")
        return

    try:
        h = {"Authorization": f"Bearer {search_token}"}
        # AUTO-ID CONVERTER: Changes Friend Code to numerical ID
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
                time.sleep(random.uniform(3, 5)) # Human delay to avoid bans
                headers = {"Authorization": f"Bearer {t}"}
                # Send View and Like
                requests.post(f"https://api.avakin.com/v1/profiles/{target_id}/views", headers=headers)
                l_res = requests.post(f"https://api.avakin.com/v1/profiles/{target_id}/likes", headers=headers)
                if l_res.status_code in [200, 201]: success += 1
        
        # Increment usage for non-VIPs
        if user_id not in VIP_USERS: 
            user_usage[user_id] += 1
            
        bot.send_message(message.chat.id, f"✅ **Complete!** Sent {success} likes/views to `{input_data}`.\nDaily Remaining: {MAX_DAILY_LIMIT - user_usage.get(user_id, 0)}")

    except Exception as e:
        bot.send_message(message.chat.id, "❌ Error: Could not find that profile. Check the code!")

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

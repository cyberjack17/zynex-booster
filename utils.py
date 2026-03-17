import time

user_last = {}

def can_use(user_id):
    now = time.time()
    if user_id not in user_last or now - user_last[user_id] > 60:
        user_last[user_id] = now
        return True
    return False
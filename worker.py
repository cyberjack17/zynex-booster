from queue import Queue
import time, random

task_queue = Queue()

def process_task(bot, message):
    msg = bot.send_message(message.chat.id, "🚀 Processing...")

    success = 0
    for i in range(10):
        success += 1
        time.sleep(random.uniform(2, 4))

        if i % 2 == 0:
            try:
                bot.edit_message_text(
                    f"⚡ Progress: {success}/10",
                    message.chat.id,
                    msg.message_id
                )
            except:
                pass

    bot.send_message(message.chat.id, f"✅ Done: {success}/10")

def worker(bot):
    while True:
        message = task_queue.get()
        try:
            process_task(bot, message)
        finally:
            task_queue.task_done()
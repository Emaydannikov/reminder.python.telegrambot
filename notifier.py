import json
import time
from datetime import datetime
from telebot import types
from config import FILENAME

def send_notifications(bot):
    while True:
        # Load reminders
        try:
            with open(FILENAME, 'r') as f:
                reminders = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            reminders = []

        for reminder in reminders:
            if reminder["status"] == "completed":
                continue

            creation_time = datetime.strptime(reminder["creation_time"], '%Y-%m-%d %H:%M:%S')
            time_since_creation = datetime.now() - creation_time

            # If the time since creation is a multiple of the frequency (modulo operation returns 0) and the reminder has times to fire left.
            if time_since_creation.total_seconds() % (reminder["frequency_hours"] * 3600) < 60 and reminder["times_to_fire"] > 0:
                markup = types.InlineKeyboardMarkup()
                done_btn = types.InlineKeyboardButton("Done", callback_data=f"done:{reminder['id']}")
                not_yet_btn = types.InlineKeyboardButton("Not Yet", callback_data=f"notyet:{reminder['id']}")
                markup.add(done_btn, not_yet_btn)

                bot.send_message(reminder["user_id"], f"Reminder: {reminder['reminder_text']}", reply_markup=markup)
                reminder["times_to_fire"] -= 1
                if reminder["times_to_fire"] == 0:
                    reminder["status"] = "completed"

        # Save reminders
        with open(FILENAME, 'w') as f:
            json.dump(reminders, f)

        time.sleep(60)

import json
import time
from datetime import datetime
from telebot import types
from config import FILENAME


HOUR_MAP = {
    1: [8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22],
    2: [8, 10, 12, 14, 16, 18, 20, 22],
    3: [8, 11, 14, 17, 20],
    4: [8, 12, 16, 20],
    5: [8, 13, 18, 23],
    6: [8, 14, 20],
    7: [8, 15, 22],
    8: [8, 16],
    9: [8, 17],
    10: [8, 18],
    11: [8, 19],
    12: [8, 20]
}
def send_notifications(bot):
    while True:
        time.sleep(60)  # Check every minute
        now = datetime.now()
        
        if now.hour < 8 or now.hour > 22:  # Do not send notifications outside the specified range
            continue

        try:
            with open(FILENAME, 'r') as f:
                reminders = json.load(f)
            
            for reminder in reminders:
                frequency = reminder['frequency_hours']

                if now.hour in HOUR_MAP[frequency]:
                    markup = types.InlineKeyboardMarkup()
                    done_btn = types.InlineKeyboardButton("Done", callback_data=f"done:{reminder['id']}")
                    not_yet_btn = types.InlineKeyboardButton("Not Yet", callback_data=f"notyet:{reminder['id']}")
                    markup.add(done_btn, not_yet_btn)

                    bot.send_message(reminder["user_id"], f"Reminder: {reminder['reminder_text']}", reply_markup=markup)
                    reminder["times_to_fire"] -= 1
                    if reminder["times_to_fire"] == 0:
                        reminder["status"] = "completed"

            with open(FILENAME, 'w') as f:
                json.dump(reminders, f)

        except (FileNotFoundError, json.JSONDecodeError):
            pass

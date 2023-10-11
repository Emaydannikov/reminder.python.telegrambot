import json
import time
from datetime import datetime
from telebot import types
from config import FILENAME

def send_notifications(bot):
    while True:
        time.sleep(60)  # Check every minute
        now = datetime.now()
        minutes_passed_in_current_hour = now.minute * 60 + now.second
        
        try:
            with open(FILENAME, 'r') as f:
                reminders = json.load(f)
            
            for reminder in reminders:
                creation_time = datetime.strptime(reminder["creation_time"], '%Y-%m-%d %H:%M:%S')
                minutes_since_creation = (now - creation_time).total_seconds() / 60
                minutes_to_next_hour = 60 - now.minute
                if reminder["times_to_fire"] > 0 and minutes_since_creation > minutes_to_next_hour and (minutes_since_creation - minutes_to_next_hour) % (reminder["frequency_hours"] * 60) < 1:
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
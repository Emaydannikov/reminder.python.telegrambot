from telebot import types
from datetime import datetime, timedelta
import json
import time

FILENAME = "reminders.json"

def send_notifications(bot):
    while True:
        reminders = []
        try:
            with open(FILENAME, 'r') as f:
                reminders = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        
        current_time = datetime.now()
        next_intervals = []
        for reminder in reminders:
            creation_time = datetime.strptime(reminder['creation_time'], '%Y-%m-%d %H:%M:%S')
            next_reminder_time = creation_time + timedelta(hours=(reminder['frequency_hours'] * (1 + int((current_time - creation_time).total_seconds() / (3600 * reminder['frequency_hours'])))))
            if current_time >= next_reminder_time:
                markup = types.InlineKeyboardMarkup()
                button = types.InlineKeyboardButton(text="Done", callback_data=f"done_{reminder['user_id']}_{reminder['creation_time']}")
                markup.add(button)
                bot.send_message(reminder['user_id'], f"Reminder: {reminder['reminder_text']}", reply_markup=markup)
                next_time = next_reminder_time + timedelta(hours=reminder['frequency_hours'])
                next_intervals.append((next_time - current_time).total_seconds())
        sleep_duration = min(next_intervals, default=60)
        time.sleep(sleep_duration)

import json
import time
from datetime import datetime

FILENAME = 'reminders.json'

def send_notifications(bot):
    while True:
        reminders = []
        try:
            with open(FILENAME, 'r') as f:
                reminders = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        
        current_time = datetime.now()
        
        for reminder in reminders:
            creation_time = datetime.strptime(reminder['creation_time'], '%Y-%m-%d %H:%M:%S')
            time_difference = current_time - creation_time
            hours_passed = time_difference.total_seconds() / 3600  

            if hours_passed % reminder['frequency_hours'] < 0.1:  
                user_id = reminder['user_id']
                bot.send_message(user_id, f"Reminder: {reminder['reminder_text']}")

        time.sleep(600)  

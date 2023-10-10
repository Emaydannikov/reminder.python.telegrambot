import telebot
import json
import threading
from config import TOKEN
from datetime import datetime
from notifier import send_notifications

bot = telebot.TeleBot(TOKEN)
user_states = {}  # To track the conversation states

FILENAME = "reminders.json"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Use /add to add a reminder, /show to list reminders, and /delete to remove one.")

@bot.message_handler(commands=['add'])
def add_reminder_step1(message):
    user_id = message.from_user.id
    user_states[user_id] = {"step": 1}
    bot.reply_to(message, "Please provide the reminder text.")

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get("step") == 1)
def add_reminder_step2(message):
    user_id = message.from_user.id
    user_states[user_id]["step"] = 2
    user_states[user_id]["reminder_text"] = message.text
    bot.reply_to(message, "How often should I remind you? (e.g., 2h, 4h, 24h)")

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get("step") == 2)
def add_reminder_step3(message):
    user_id = message.from_user.id
    frequency = message.text.rstrip("h")

    if frequency.isdigit():
        frequency_hours = int(frequency)

        creation_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        reminder = {
            "user_id": user_id,
            "creation_time": creation_time,
            "reminder_text": user_states[user_id]["reminder_text"],
            "frequency_hours": frequency_hours
        }

        reminders = []
        try:
            with open(FILENAME, 'r') as f:
                reminders = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        reminders.append(reminder)

        with open(FILENAME, 'w') as f:
            json.dump(reminders, f)

        bot.reply_to(message, f"Added reminder: {reminder['reminder_text']} to remind every {frequency_hours} hours.")
        del user_states[user_id]  # Remove user state after completing the process

    else:
        bot.reply_to(message, "Invalid format. Please enter a valid frequency (e.g., 2h, 4h, 24h).")

@bot.message_handler(commands=['show'])
def show_reminders(message):
    user_id = message.from_user.id 

    reminders = []
    try:
        with open(FILENAME, 'r') as f:
            reminders = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    user_reminders = [r for r in reminders if r['user_id'] == user_id]

    if user_reminders:
        reminder_texts = [f"Text: {r['reminder_text']} | Frequency: {r['frequency_hours']} hours | Created: {r['creation_time']}" for r in user_reminders]
        reminder_list = '\n'.join(reminder_texts)
        bot.reply_to(message, reminder_list)
    else:
        bot.reply_to(message, "You have no reminders set.")

@bot.message_handler(commands=['delete'])
def delete_reminder(message):
    index_text = message.text.split("/delete ", 1)[-1]
    if index_text.isdigit():
        index = int(index_text)
        with open(FILENAME, 'r') as f:
            reminders = json.load(f)
        if 0 <= index < len(reminders):
            removed = reminders.pop(index)
            with open(FILENAME, 'w') as f:
                json.dump(reminders, f)
            bot.reply_to(message, f"Deleted reminder: {removed}")
        else:
            bot.reply_to(message, "Please provide a valid reminder index to delete.")
    else:
        bot.reply_to(message, "Please provide a valid reminder index to delete.")


if __name__ == "__main__":
    t = threading.Thread(target=send_notifications)
    t.start()
    bot.polling(none_stop=True)

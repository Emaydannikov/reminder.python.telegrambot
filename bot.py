import telebot
import json
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

FILENAME = "reminders.json"

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Hello! Use /add to add a reminder, /show to list reminders, and /delete to remove one.")

@bot.message_handler(commands=['add'])
def add_reminder(message):
    reminder = message.text.split("/add ", 1)[-1]
    if reminder and reminder != "/add":
        reminders = []
        try:
            with open(FILENAME, 'r') as f:
                reminders = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            pass

        reminders.append(reminder)

        with open(FILENAME, 'w') as f:
            json.dump(reminders, f)
        
        bot.reply_to(message, f"Added reminder: {reminder}")
    else:
        bot.reply_to(message, "Please provide the reminder text after /add")

@bot.message_handler(commands=['show'])
def show_reminders(message):
    reminders = []
    try:
        with open(FILENAME, 'r') as f:
            reminders = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass
    if reminders:
        reminder_list = '\n'.join(reminders)
        bot.reply_to(message, reminder_list)
    else:
        bot.reply_to(message, "No reminders found.")

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
    bot.polling(none_stop=True)
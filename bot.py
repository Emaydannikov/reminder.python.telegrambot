from config import TOKEN, FILENAME
import telebot
from telebot import types
import json
from datetime import datetime
import random
import string

bot = telebot.TeleBot(TOKEN)
user_states = {}


def generate_id(length=8):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for i in range(length))


def generate_markup():
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("Add Reminder", callback_data="add")
    item2 = types.InlineKeyboardButton("View Reminders", callback_data="view")
    item3 = types.InlineKeyboardButton(
        "Delete Reminder", callback_data="delete")
    markup.add(item1, item2, item3)
    return markup


@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = generate_markup()
    bot.send_message(
        message.chat.id, "Welcome! What would you like to do?", reply_markup=markup)


@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data == "add":
        bot.answer_callback_query(call.id)
        user_states[call.from_user.id] = {"step": 1}
        bot.send_message(call.from_user.id,
                         "Please provide the reminder text.")
    elif call.data == "view":
        bot.answer_callback_query(call.id)
        view_reminders(call.from_user.id)
    elif call.data == "delete":
        bot.answer_callback_query(call.id)
        user_states[call.from_user.id] = {"step": "delete"}
        bot.send_message(
            call.from_user.id, "Please provide the ID of the reminder you want to delete.")


def view_reminders(user_id):
    reminders = []
    try:
        with open(FILENAME, 'r') as f:
            reminders = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    user_reminders = [
        reminder for reminder in reminders if reminder["user_id"] == user_id]
    if not user_reminders:
        bot.send_message(user_id, "You have no reminders.")
        return

    for reminder in user_reminders:
        bot.send_message(user_id, f"ID: {reminder['id']}\nReminder: {reminder['reminder_text']}\nFrequency: Every {
                         reminder['frequency_hours']} hour(s)\nTimes to fire: {reminder['times_to_fire']} times\nStatus: {reminder['status']}")


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get("step") == 1)
def add_reminder_step2(message):
    user_id = message.from_user.id
    user_states[user_id]["reminder_text"] = message.text
    bot.send_message(
        user_id, "How often should I remind you? (e.g., 2h, 4h, 24h)")
    user_states[user_id]["step"] = 2


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get("step") == 2)
def add_reminder_step3(message):
    user_id = message.from_user.id
    frequency = message.text.rstrip("h")
    if frequency.isdigit():
        user_states[user_id]["frequency_hours"] = int(frequency)
        bot.send_message(
            user_id, "How many times should the notification fire? (Input a number or 'infinite')")
        user_states[user_id]["step"] = 3
    else:
        bot.send_message(
            user_id, "Invalid format. Please enter a valid frequency (e.g., 2h, 4h, 24h).")


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get("step") == 3)
def add_reminder_step4(message):
    user_id = message.from_user.id
    if message.text.isdigit() or message.text == "infinite":
        times_to_fire = int(message.text) if message.text.isdigit() else 9999
        user_states[user_id]["times_to_fire"] = times_to_fire

        reminder = {
            "id": generate_id(),
            "user_id": user_id,
            "creation_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "reminder_text": user_states[user_id]["reminder_text"],
            "frequency_hours": user_states[user_id]["frequency_hours"],
            "times_to_fire": user_states[user_id]["times_to_fire"],
            "status": "not completed"
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

        bot.send_message(user_id, f"Added reminder: {reminder['reminder_text']} to remind every {
                         reminder['frequency_hours']} hour(s) for {reminder['times_to_fire']} times.")
        del user_states[user_id]
        send_welcome(message)
    else:
        bot.send_message(
            user_id, "Invalid input. Please enter a valid number or 'infinite'.")


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id, {}).get("step") == "delete")
def delete_reminder(message):
    user_id = message.from_user.id
    reminder_id = message.text

    reminders = []
    try:
        with open(FILENAME, 'r') as f:
            reminders = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        pass

    reminder_to_delete = next(
        (reminder for reminder in reminders if reminder["id"] == reminder_id and reminder["user_id"] == user_id), None)
    if reminder_to_delete:
        reminders.remove(reminder_to_delete)
        with open(FILENAME, 'w') as f:
            json.dump(reminders, f)
        bot.send_message(user_id, f"Deleted reminder: {
                         reminder_to_delete['reminder_text']}")
        del user_states[user_id]
    else:
        bot.send_message(user_id, "No such reminder found.")


bot.polling(none_stop=True)

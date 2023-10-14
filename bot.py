from config import TOKEN
from json_proc import create_notification, get_notifications_for_user, format_notification, get_notification_by_id_or_text, delete_notification_by_id, load_notifications, save_notifications
import telebot
import threading
import time

bot = telebot.TeleBot(TOKEN)
user_data = {}
user_delete_data = {}


def send_reply(message, text):
    bot.reply_to(message, text)


def send_message(chat_id, text):
    bot.send_message(chat_id, text)


def delete_user_message(message):
    chat_id = message.chat.id
    message_id = message.message_id
    try:
        bot.delete_message(chat_id, message_id)
    except Exception as e:
        print(f"Failed to delete message: {e}")


@bot.message_handler(commands=['start'])
def send_welcome(message):
    delete_user_message(message)
    send_message(message.chat.id,
                 "Welcome! Use the following commands:\n/start - to see welcome message\n/new - to create a new notification\n/view - to view saved notifications\n/delete - to delete notifications")


@bot.message_handler(commands=['new'])
def new_notification_command(message):
    user_id = message.from_user.id
    user_data[user_id] = {}
    send_message(message.chat.id, "Please enter the notification text:")


@bot.message_handler(func=lambda message: message.from_user.id in user_data and 'text' not in user_data[message.from_user.id])
def get_text(message):
    user_id = message.from_user.id
    user_data[user_id]['text'] = message.text
    send_message(message.chat.id,
                 "Please specify how often you want to receive notifications (in hours):")


@bot.message_handler(func=lambda message: message.from_user.id in user_data and 'text' in user_data[message.from_user.id] and 'frequency' not in user_data[message.from_user.id])
def get_frequency(message):
    user_id = message.from_user.id
    try:
        frequency = float(message.text)
        user_data[user_id]['frequency'] = frequency * 60
        send_message(
            message.chat.id, "Please specify the total number of notifications you want to receive:")
    except ValueError:
        send_message(message.chat.id, "Invalid input. Please enter a number.")


@bot.message_handler(func=lambda message: message.from_user.id in user_data and 'frequency' in user_data[message.from_user.id] and 'total_count' not in user_data[message.from_user.id])
def get_total_count(message):
    user_id = message.from_user.id
    try:
        total_count = int(message.text)
        user_data[user_id]['total_count'] = total_count
        notification = create_notification(
            user_id, user_data[user_id]['text'], user_data[user_id]['frequency'], total_count)
        send_message(message.chat.id, f"Notification created with ID: {
                     notification['notification_id']}")
        del user_data[user_id]
    except ValueError:
        send_message(message.chat.id,
                     "Invalid input. Please enter an integer.")


@bot.message_handler(commands=['view'])
def view_notifications(message):
    user_id = message.from_user.id
    user_notifications = get_notifications_for_user(user_id)

    if not user_notifications:
        send_message(message.chat.id, "You have no notifications.")
        return

    for notification in user_notifications:
        formatted_notification = format_notification(notification)
        send_message(message.chat.id, formatted_notification)


@bot.message_handler(commands=['delete'])
def prompt_delete_notification(message):
    user_id = message.from_user.id
    user_notifications = get_notifications_for_user(user_id)

    if not user_notifications:
        send_message(message.chat.id, "You have no notifications.")
        return

    info_messages = [f"ID: {n['notification_id']
                            } - Text: {n['text']}" for n in user_notifications]
    for msg in info_messages:
        send_message(message.chat.id, msg)

    send_message(message.chat.id,
                 "Please enter the Notification ID or text of the notification you want to delete.")
    user_delete_data[user_id] = "awaiting_delete_confirmation"


@bot.message_handler(func=lambda message: message.from_user.id in user_delete_data and user_delete_data[message.from_user.id] == "awaiting_delete_confirmation")
def process_delete(message):
    user_id = message.from_user.id
    identifier = message.text

    notification = get_notification_by_id_or_text(user_id, identifier)
    if notification:
        delete_notification_by_id(notification['notification_id'])
        send_message(message.chat.id, f"Notification (Text: '{
                     notification['text']}' - ID: {notification['notification_id']}) has been successfully deleted.")
        del user_delete_data[user_id]
    else:
        send_message(
            message.chat.id, "No notification found with the provided ID or text. Please try again.")


def notification_worker():
    while True:
        notifications = load_notifications()
        current_time = time.time()

        for notification in notifications:
            if notification['status'] == 'active' and notification['next_notification_time'] <= current_time:
                send_notification_to_user(notification)
                update_notification_after_sending(notification)

        time.sleep(10)  # Check every 10 seconds


def send_notification_to_user(notification):
    user_id = notification['user_id']
    Reminder = f"Reminder: {notification['text']}"
    send_message(user_id, Reminder)


def update_notification_after_sending(notification):
    notification['sent_count'] += 1
    notification['next_notification_time'] += notification['frequency'] * 60

    if notification['sent_count'] >= notification['total_count']:
        notification['status'] = 'inactive'

    notifications = load_notifications()
    updated_notifications = [n if n['notification_id'] !=
                             notification['notification_id'] else notification for n in notifications]
    save_notifications(updated_notifications)


notification_thread = threading.Thread(target=notification_worker)
notification_thread.start()
if __name__ == '__main__':
    bot.polling(none_stop=True)

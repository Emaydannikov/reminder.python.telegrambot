import json
from datetime import datetime, timedelta
from config import FILE_NAME
from support_func import generate_id


def load_notifications():
    try:
        with open(FILE_NAME, 'r') as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_notifications(data):
    with open(FILE_NAME, 'w') as file:
        json.dump(data, file, indent=4)


def datetime_to_timestamp(dt):
    """Convert a datetime object to a Unix timestamp."""
    return dt.timestamp()


def timestamp_to_datetime(ts):
    """Convert a Unix timestamp to a datetime object."""
    return datetime.fromtimestamp(ts)


def create_notification(user_id, text, frequency, total_count):
    current_time = datetime.now()
    notification = {
        "notification_id": str(generate_id()),
        "user_id": user_id,
        "text": text,
        "time_sent": datetime_to_timestamp(current_time),
        "frequency": frequency,
        "total_count": total_count,
        "sent_count": 0,
        "next_notification_time": datetime_to_timestamp(current_time + parse_frequency(frequency)),
        "status": "active"
    }
    notifications = load_notifications()
    notifications.append(notification)
    save_notifications(notifications)
    return notification


def parse_frequency(frequency):
    return timedelta(minutes=int(frequency))


def get_notifications_for_user(user_id):
    notifications = load_notifications()
    user_notifications = [n for n in notifications if n['user_id'] == user_id]
    return user_notifications


def format_notification(notification):
    """Format a notification for display."""
    next_time = timestamp_to_datetime(notification['next_notification_time'])
    formatted_next_time = next_time.strftime(
        '%Y-%m-%d %H:%M:%S')  # Format as needed
    return (
        f"Notification ID: {notification['notification_id']}\n"
        f"Text: {notification['text']}\n"
        f"Frequency: {notification['frequency']} minutes\n"
        f"Total Count: {notification['total_count']}\n"
        f"Sent Count: {notification['sent_count']}\n"
        f"Next Notification Time: {formatted_next_time}\n"
        f"Status: {notification['status']}"
    )


def get_notification_by_id_or_text(user_id, identifier):
    notifications = get_notifications_for_user(user_id)
    for notification in notifications:
        if notification['notification_id'] == identifier or notification['text'] == identifier:
            return notification
    return None


def delete_notification_by_id(notification_id):
    notifications = load_notifications()
    updated_notifications = [
        n for n in notifications if n['notification_id'] != notification_id]
    save_notifications(updated_notifications)

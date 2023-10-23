from telebot import types

def start_menu():
    markup = types.InlineKeyboardMarkup()
    
    btn_language = types.InlineKeyboardButton("Select Language", callback_data="select_language")
    btn_time_zone = types.InlineKeyboardButton("Select Time Zone", callback_data="select_time_zone")
    btn_main_menu = types.InlineKeyboardButton("Main Menu", callback_data="main_menu")

    markup.row(btn_language)
    markup.row(btn_time_zone)
    markup.row(btn_main_menu)
    
    return markup

def language_menu():
    markup = types.InlineKeyboardMarkup()
    
    btn_russian = types.InlineKeyboardButton("Русский", callback_data="language_russian")
    btn_english = types.InlineKeyboardButton("English", callback_data="language_english")
    btn_back = types.InlineKeyboardButton("Back to Start", callback_data="start_menu")

    markup.row(btn_russian)
    markup.row(btn_english)
    markup.row(btn_back)
    
    return markup

def main_menu():
    markup = types.InlineKeyboardMarkup()
    
    btn_new_notification = types.InlineKeyboardButton("New Notification", callback_data="new_notification")
    btn_view_notifications = types.InlineKeyboardButton("View Notifications", callback_data="view_notifications")
    btn_edit_notifications = types.InlineKeyboardButton("Edit Notifications", callback_data="edit_notifications")
    btn_delete_notifications = types.InlineKeyboardButton("Delete Notifications", callback_data="delete_notifications")
    btn_back = types.InlineKeyboardButton("Back to Start", callback_data="start_menu")
    
    markup.row(btn_new_notification)
    markup.row(btn_view_notifications)
    markup.row(btn_edit_notifications)
    markup.row(btn_delete_notifications)
    markup.row(btn_back)
    
    return markup


def timezone_menu():
    markup = types.InlineKeyboardMarkup()

    # Generate buttons for GMT -1 to GMT +5
    for i in range(-1, 6):
        if i < 0:
            btn = types.InlineKeyboardButton(f"GMT {i}", callback_data=f"timezone_gmt{i}")
        else:
            btn = types.InlineKeyboardButton(f"GMT +{i}", callback_data=f"timezone_gmt+{i}")
        markup.row(btn)

    btn_back = types.InlineKeyboardButton("Back to Start", callback_data="start_menu")
    markup.row(btn_back)

    return markup
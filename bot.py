import telebot
from markups import start_menu, main_menu, language_menu, timezone_menu
from config import TOKEN

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):    
    bot.send_message(message.chat.id, "Welcome! Please choose:", reply_markup=start_menu())

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "main_menu":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Main Menu:", reply_markup=main_menu())
    elif call.data == "start_menu":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Welcome! Please choose:", reply_markup=start_menu())
    elif call.data == "select_language":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Select a language:", reply_markup=language_menu())
    elif call.data == "select_time_zone":
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Select a time zone:", reply_markup=timezone_menu())

bot.polling()
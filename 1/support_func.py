# Support functions
import string
import random
import logging
from telebot import types


# Generating ID for notification with random 5 symbols
def generate_id(length=5):
    chars = string.ascii_lowercase + string.digits
    return ''.join(random.choice(chars) for i in range(length))


# Generating buttons
def generate_markup():
    markup = types.InlineKeyboardMarkup()
    item1 = types.InlineKeyboardButton("✅ Add", callback_data="add")
    item2 = types.InlineKeyboardButton("✳️ View", callback_data="view")
    item3 = types.InlineKeyboardButton("❎ Delete", callback_data="delete")
    markup.add(item1, item2, item3)
    return markup


def setup_logging():
    logging.basicConfig(filename='bot.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logger = logging.getLogger()
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console.setFormatter(formatter)
    logger.addHandler(console)

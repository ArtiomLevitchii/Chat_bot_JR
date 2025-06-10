from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging

logger = logging.getLogger(__name__)

def get_main_menu_keyboard():
    buttons = [
            [InlineKeyboardButton("Random fact", callback_data="random_fact")],
            [InlineKeyboardButton("ChatGPT(soon)", callback_data="chat_gpt")],
            [InlineKeyboardButton("Chat with celebrity(soon)", callback_data="chat_with_celebrity")],
            [InlineKeyboardButton("Quiz(soon)", callback_data="quiz")],
    ]
    return InlineKeyboardMarkup(buttons)

def get_one_more_fact_keyboard():
    buttons = [
            [InlineKeyboardButton("One more fact", callback_data="random_more")],
            [InlineKeyboardButton("END", callback_data="random_exit")]
    ]
    return InlineKeyboardMarkup(buttons)
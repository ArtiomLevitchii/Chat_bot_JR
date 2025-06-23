"""Модуль с функциями генерации клавиатур для Telegram-бота."""

from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import logging

logger = logging.getLogger(__name__)

def get_main_menu_keyboard():
    """Вовзращает основную клавиатуру"""
    buttons = [
            [InlineKeyboardButton("🎲 Random fact", callback_data="random_fact")],
            [InlineKeyboardButton("💬 Chat with AI", callback_data="chat_gpt")],
            [InlineKeyboardButton("🌟 Chat with celebrity", callback_data="chat_with_celebrity")],
            [InlineKeyboardButton("🧠 Quiz", callback_data="start_quiz_with_user")],
            [InlineKeyboardButton("🌐 Audio/Voice translator", callback_data="start_translator")],
            [InlineKeyboardButton("🏃🏻 Sports(proteins/fats/carbohydrates/calories) counter 💪", callback_data="meal_counter")]
    ]
    return InlineKeyboardMarkup(buttons)

def get_one_more_fact_keyboard():
    """Вовзращает дополнительную клавиатуру для рандомного факта"""
    buttons = [
            [InlineKeyboardButton("🔁 One more fact", callback_data="random_more")],
            [InlineKeyboardButton("❌ END", callback_data="random_exit")]
    ]
    return InlineKeyboardMarkup(buttons)

def get_buttons_for_themes(list):
    """Вовзращает клавиатуру с масштабируемым списком тем"""
    buttons = [
            [InlineKeyboardButton(f"🧠  {value} ", callback_data=f"quiz_theme_{index}")]
        for index, value in enumerate(list)
    ]
    return InlineKeyboardMarkup(buttons)

def get_difficulty_buttons():
    """Вовзращает клавиатуру для выбора сложности"""
    buttons = [
        [InlineKeyboardButton("🟢 Easy", callback_data="difficulty_easy")],
        [InlineKeyboardButton("🟡 Medium", callback_data="difficulty_medium")],
        [InlineKeyboardButton("🔴 Hard", callback_data="difficulty_hard")]
    ]
    return InlineKeyboardMarkup(buttons)

def get_answers_buttons(list):
    """Вовзращает клавиатуру с масштабируемым списком ответов"""
    buttons = [
        [InlineKeyboardButton(f"{index}. {value}", callback_data=f"question_answer_{value}")]
        for index, value in enumerate(list)
    ]
    return InlineKeyboardMarkup(buttons)

def continue_quiz_exit():
    """Вовзращает дополнительную клавиатуру для квиза"""
    buttons = [
        [InlineKeyboardButton("🔁 One more question", callback_data="continue_quiz")],
        [InlineKeyboardButton("🔁 Select other quiz theme", callback_data="select_quiz_theme")],
        [InlineKeyboardButton("❌ END", callback_data="quiz_exit")]
    ]
    return InlineKeyboardMarkup(buttons)
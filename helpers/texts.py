"""Модуль с функциями генерации основного текста и текста об ошибке"""

import logging

logger = logging.getLogger(__name__)

def get_main_text_menu() -> str:
    """Возвращает основной текст"""
    return ("👋 <b>Welcome to ChatGpt bot</b>\n\n"
        "<b>Available options</b>\n"
        "🎲 Random fact - get a random fact from AI\n"
        "💬 ChatGPT - take a talk with AI(soon)\n"
        "🌟 Chat with celebrity - take a talk with a celebrity(soon)\n"
        "🧠 Quiz - check your knowledge(soon)\n"
        "Choose option from menu to continue:"
            )

def get_user_error_message() -> str:
    """Возвращает текст об ошибке"""
    return ("🛑🛑🛑 An error occurred - try later. Use 🚀 /start to follow main menu🛑🛑🛑")
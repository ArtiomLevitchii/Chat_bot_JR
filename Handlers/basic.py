import asyncio
import logging
from  telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from helpers.keyboards import get_main_menu_keyboard,get_one_more_fact_keyboard
from helpers.texts import get_main_text_menu

logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for start"""

    reply_markup = get_main_menu_keyboard()

    welcome_text = get_main_text_menu()

    await update.message.reply_text(welcome_text,parse_mode='HTML',reply_markup=reply_markup)

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for selection"""
    query = update.callback_query

    await query.answer()

    if query.data == "random_fact":
        """Call from random_fact.py"""
        pass
    elif query.data == "chat_gpt":
        await query.edit_message_text(
            "<b>ChatGpt activated</b>\n\n"
            "Write me anything"
            ,parse_mode='HTML'
        )
    elif query.data in ["chat_with_celebrity","quiz"]:
        await query.edit_message_text(
            "<b>COMING SOON</b>\n\n",
            parse_mode='HTML'
        )

        await asyncio.sleep(3)
        await start_menu_again(query)

async def start_menu_again(query):
    """Return back start menu"""

    reply_markup = get_main_menu_keyboard()

    await query.edit_message_text(
        "<b>Welcome to ChatGPT bot</b>\n\n"
        "Choose option from menu to continue:",
        parse_mode='HTML',
        reply_markup=reply_markup
    )

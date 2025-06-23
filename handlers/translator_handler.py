"""Модуль для обработки аудио и голосовых сообщений с последующим переводом с помощью AI."""

import logging

from telegram import Update
from telegram.ext import ContextTypes
from helpers.texts import get_user_error_message
import os
from  services.openai_client import recognize_and_translate
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from pathlib import Path

logger = logging.getLogger(__name__)

async def start_translator(update:Update, context:ContextTypes.DEFAULT_TYPE):
    """
        Обрабатывает аудио/голосовое сообщение, передаёт его в OpenAI для распознавания и перевода.
        """
    try:
        message = update.message

        if not message:
            if update.callback_query:
                await update.message.reply_text(
                    "<b>This is not an voice or audio file!</b>",
                    parse_mode='HTML'
                )
                return

        audio = update.message.voice or update.message.audio

        if not audio:
            await update.message.reply_text(
                "<b>This is not an voice or audio file!</b>",
                parse_mode='HTML'
            )
            return

        file = await audio.get_file()
        file_path = f"temp_{update.effective_user.id}.ogg"

        await file.download_to_drive(file_path)

        loading_gif_path = Path("images/loading_icon.gif")

        loading_message = await update.message.reply_animation(
            animation=loading_gif_path.open("rb"),
            caption="⏳ Loading..."
        )

        await recognize_and_translate(file_path, update, context)
        await loading_message.delete()
        await update.message.reply_text(
            "\n",
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ exit to main menu ❌", callback_data="/exit")]])
        )

        os.remove(file_path)
    except Exception as e:
        logger.error(f"🛑🛑🛑An error occurred while audio is pre worked - {e}🛑🛑🛑")
        await update.message.reply_text(get_user_error_message())
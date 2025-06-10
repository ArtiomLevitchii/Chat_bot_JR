import logging
from services.openai_client import responce_to_user_message
from telegram import Update
from telegram.ext import ContextTypes

logger = logging.getLogger(__name__)


async def response_to_user(update: Update, context:ContextTypes.DEFAULT_TYPE):

    try:
        user_message = update.message.text

        ai_response = await responce_to_user_message(user_message)

        await update.message.reply_text(ai_response)
    except Exception as e:
        logger.error(f"An error occurred while AI generated respose to user - {e}")
        return "AI services are unavailable now, try again later"
from telegram import Update
from telegram.ext import ContextTypes
from . import chat_with_AI, chat_with_celebrity

import logging

logger = logging.getLogger(__name__)

async def message_router(update: Update, context:ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("celebrity_chat_active") or context.user_data.get("awaiting_celebrity_name"):
       await chat_with_celebrity.start_chat_with_celebrity(update,context)
    elif context.user_data.get("chat_mode"):
        await chat_with_AI.response_to_user(update,context)
    else:
        await update.message.reply_text("🟢 Choose option from menu or use 🚀 /start")


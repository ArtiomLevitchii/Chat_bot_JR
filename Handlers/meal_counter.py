import asyncio
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from helpers.texts import get_user_error_message
from services.openai_client import count_meal_basics
from pathlib import Path
logger = logging.getLogger(__name__)

async def start_meal_counter(update:Update,context:ContextTypes.DEFAULT_TYPE):
    try:
        query = update.callback_query
        await query.answer()
        image_path = Path("images/foto_1_py.jpg")
        with open(image_path,"rb") as photo:
            await query.message.chat.send_photo(photo=photo)

        await asyncio.sleep(1)
        logger.info("meal_counter_started")

        context.user_data["meal_counter_step"] = "age"

        await query.edit_message_text("📆 Enter your age: 📆 ")


    except Exception as e:
        logger.error(f"🛑🛑🛑An error occurred while was starting meal counter - {e}🛑🛑🛑")
        await update.callback_query.message.reply_text(get_user_error_message())


async def meal_counter_conversation(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_data = context.user_data
        step = user_data.get("meal_counter_step")

        text = update.message.text.strip()

        if step == "age":
            if not text.isdigit():
                await update.message.reply_text("📆 Enter your age (example : 30) 📆")
                return

            user_data["age"] = int(text)
            user_data["meal_counter_step"] = "weight"
            await update.message.reply_text("🤦‍♂️ Enter your weight (example : 75) 🤦‍♂️")

        elif step == "weight":
            if not text.isdigit():
                await update.message.reply_text("🤦‍♂️ Enter your weight (example : 75) 🤦‍♂️")
                return

            user_data["weight"] = int(text)
            user_data["meal_counter_step"] = "height"
            await update.message.reply_text("🧍‍♂️ Enter your height (example : 175) 🧍‍♂️")

        elif step == "height":
            if not text.isdigit():
                await update.message.reply_text("🧍‍♂️ Enter your height (example : 175) 🧍‍♂️")
                return

            user_data["height"] = int(text)
            user_data["meal_counter_step"] = "gender"
            await update.message.reply_text("🤵‍♂ Enter your gender (example : M/F or Male/Female or М/Ж or Мужчина/Женщина) 👰‍♀️")

        elif step == "gender":
            if text.lower() not in ["m","f","male","female","м","ж","мужчина","женщина"]:
                await update.message.reply_text("🤵‍♂ Enter your gender (example : M/F or Male/Female or М/Ж or Мужчина/Женщина) 👰‍♀️")
                return

            user_data["gender"] = text
            user_data["meal_counter_step"] = "sports"
            await update.message.reply_text("🏃🏻 Enter your sports (example : armwrestling/армрестлинг) 💪")

        elif step == "sports":
            if text.isdigit():
                await update.message.reply_text("🏃🏻 Enter your sports (example : armwrestling/армрестлинг) 💪")

            user_data["sports"] = text
            user_data["meal_counter_step"] = None


            await update.message.reply_text(
                f"<b>😊 Nice!</b> Your age is - {user_data["age"]}🙋‍♂️\n"
                f"🧍‍♂️Your height is - {user_data["height"]}🧍‍♂️\n"
                f"🤦‍♂️Your weight is - {user_data["weight"]}🤦‍♂️\n"
                f"🤵‍♂️Your gender is - {user_data["gender"]}👰‍♀️\n"
                f"🏃🏻 Your sport is - {user_data["sports"]} 💪\n",
                parse_mode='HTML'
            )

            await update.message.reply_text("COUNTING...")

            result = await count_meal_basics(user_data["age"],user_data["height"],user_data["weight"],user_data["gender"],user_data["sports"])
            await update.message.reply_text(
                "<b>YOUR meal goal for 1 day:</b>\n\n"
                f"{result}",
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("❌ exit to main menu ❌", callback_data="/exit")]])
            )

        else:
            await update.message.reply_text("To enter one more time data, press /start")
    except Exception as e:
        logger.error(f"🛑🛑🛑An error occurred while collecting meal data - {e}🛑🛑🛑")
        await update.message.reply_text(get_user_error_message())
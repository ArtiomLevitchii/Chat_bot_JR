import logging
from telegram.ext import Application, CommandHandler, CallbackQueryHandler,MessageHandler,filters
from config import TELEGRAM_BOT_KEY
from Handlers import basic, random_fact,chat_with_AI


#Adding basic configuration for log actions in console
logging.basicConfig(
    format="%(asctime)s - %(name)s -%(levelname)s -%(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    try:
        application = Application.builder().token(TELEGRAM_BOT_KEY).build()

        application.add_handler(CommandHandler("start", basic.start))

        application.add_handler(CommandHandler("random", random_fact.random_fact))
        application.add_handler(CallbackQueryHandler(random_fact.random_fact_callback, pattern="random_"))

        application.add_handler(CallbackQueryHandler(basic.menu_callback))

        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat_with_AI.response_to_user))

        logger.info("Chat bot was successfully started")
        application.run_polling()
    except Exception as e:
        logger.info(f"An error occurred while starting bot - {e}")

if __name__  == "__main__":
    main()
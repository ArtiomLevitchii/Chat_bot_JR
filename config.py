import os

from dotenv import load_dotenv

load_dotenv()

CHAT_GPT_KEY = os.getenv("CHAT_GPT_KEY")
TELEGRAM_BOT_KEY = os.getenv("TELEGRAM_BOT_KEY")

if not all([CHAT_GPT_KEY,TELEGRAM_BOT_KEY]):
    raise ValueError("Tokens not found in .env")
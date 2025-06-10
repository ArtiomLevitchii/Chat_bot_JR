import logging

from openai import AsyncOpenAI
from config import CHAT_GPT_KEY

logger = logging.getLogger(__name__)
client = AsyncOpenAI(api_key=CHAT_GPT_KEY)

async def get_random_fact():
    """AI Generates random fact"""
    try:
        responce = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are assistant, who tells interesting facts, you speak in russian"
                },
                {
                    "role": "user",
                    "content": "Tell interesting fact, doesn't matter from what region"
                }
            ],
            max_tokens=200,
            temperature=0.8
        )

        fact = responce.choices[0].message.content.strip()

        logger.info(f"Fact was successfully generated - {fact}")
        return fact
    except Exception as e:
        logger.error(f"An error occurred while fact was generating - {e}")
        return "Unfortunately AI serices are unavailable now, try later"

async def responce_to_user_message(user_message: list[dict]) -> str:
    """AI responces random fact"""
    try:
        result = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are like a friend to user, responce him in russian"
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=500,
            temperature=1
        )
        return result.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error occurred with chat service - {e}")
        return "Unfortunately AI service are unavailable now, try later"

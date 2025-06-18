import logging

from openai import AsyncOpenAI
from config import CHAT_GPT_KEY
from chat_history.chat_with_user import chat_with_user

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
        return "🛑🛑🛑Unfortunately AI serices are unavailable now, try later🛑🛑🛑"

async def responce_to_user_message(user_message: list[dict]) -> str:
    """AI responses"""
    try:
        result = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=user_message,
            max_tokens=500,
            temperature=1
        )
        return result.choices[0].message.content.strip()
    except Exception as e:
        logger.error(f"Error occurred with chat service - {e}")
        return "🛑🛑🛑Unfortunately AI service are unavailable now, try later🛑🛑🛑"


async def generate_celebrity_prompt(name: str) -> str:
    prompt = (
        f"Find who is this {name}. Give short description about this person, what is he/she famous about."
        "If it is famous person, response in russian. Don't make things up, if there is no information or it's not a very famous person, say - не нашлось"
    )

    for _ in range(3):
        try:
            response = await client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are assistant, who search information about famous people. Response shortly in russian"
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=300,
                temperature=0.7
            )

            content = response.choices[0].message.content.strip().lower()

            if "не нашлось" in content or "не удалось" in content or len(content) < 30:
                continue

            return f"Ты теперь {name}. {response.choices[0].message.content.strip()} \n Response in first person, friendly, response in russian."
        except Exception as e:
            logger.error(f"Error occurred with chat service - {e}")

    return None


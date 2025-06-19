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

async def generate_quiz_themes():
    prompt = (
        "You need to generate themes for small quiz for user. Themes must be of medium difficulty. "
        "Write them in a list each on a new line, without extra explanations, i'll use this list to make buttons for themes, for selection. Always response in russian"
    )

    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=300,
            temperature=0.3,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that creates themes for quiz, always response in russian"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response.choices[0].message.content.strip()
        return content
    except Exception as e:
        logger.error(f"Error occurred with themes generator service - {e}")
        return "🛑🛑🛑Failed to generate quiz themes. Try later or use 🚀 /start 🛑🛑🛑"

async def generate_question(theme, complexity):
    prompt = (
        f"Generate question for this theme - {theme} with this complexity - {complexity}"
        "Question must be only in russian"
    )

    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=900,
            temperature=1,
            messages=[
                {
                    "role": "system",
                    "content": "You are assistant that find question for quiz, always response in russian"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        content = response.choices[0].message.content.strip()

        return content
    except Exception as e:
        logger.error(f"Error occurred with question generator service - {e}")
        return "🛑🛑🛑Failed to generate question. Try later or use 🚀 /start 🛑🛑🛑"

async def generate_answers_for_question(question):
    prompt = (
        f"Generate 4 answers for this question - {question}. One of them must be correct answer. Don't specify which answer is correct."
        "Write them in list. Must be 4 separate words or expressions. Answers must be only in russian"
    )

    try:
        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=50,
            temperature=1,
            messages=[
                {
                    "role": "system",
                    "content": "You are assistant who generates answers for question. Response only in russian"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        result = response.choices[0].message.content.strip()
        return result
    except Exception as e:
        logger.error(f"Error occurred with answers generator service - {e}")
        return "🛑🛑🛑Failed to generate quiz answers. Try later or use 🚀 /start 🛑🛑🛑"

async def verify_answer_AI(question, answer):

    try:

        prompt = (
            f"You must verify if this answer - {answer} is correct to this question - {question}"
            "If answer is correct return True, if is wrong return False"
        )

        response = await client.chat.completions.create(
            model="gpt-3.5-turbo",
            max_tokens=20,
            temperature=1,
            messages=[
                {
                    "role": "system",
                    "content": "You are assistant, you must verify if answer is correct"
                },
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        result_raw = response.choices[0].message.content.strip().lower()

        if "true" in result_raw or "да" in result_raw:
            return True
        elif "false" in result_raw or "нет" in result_raw:
            return False
        else:
            return False
    except Exception as e:
        logger.error(f"Error occurred with answers verification service - {e}")
        return "🛑🛑🛑Failed to verify quiz answers. Try later or use 🚀 /start 🛑🛑🛑"
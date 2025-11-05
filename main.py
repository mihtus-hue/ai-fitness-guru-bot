import os
import openai
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# === Настройки ===
TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

openai.api_key = OPENAI_API_KEY

bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()

# Память пользователей
user_memory = {}

@dp.message(Command("start"))
async def start_command(message: Message):
    user_memory[message.from_user.id] = []
    await message.answer(
        "🏋️ Привет! Я — твой AI Fitness-гуру. "
        "Расскажи немного о себе: возраст, цели и текущая форма."
    )

@dp.message()
async def chat_with_user(message: Message):
    user_id = message.from_user.id
    user_memory.setdefault(user_id, [])

    user_message = message.text.strip()
    user_memory[user_id].append({"role": "user", "content": user_message})
    conversation = user_memory[user_id]

    try:
        # GPT анализирует контекст и эмоции
        system_prompt = (
            "Ты — фитнес-тренер и психолог, который умеет чувствовать настроение собеседника. "
            "Говори естественно, без шаблонов, с живыми фразами. "
            "Если человек устал — поддержи. Если он вдохновлён — усили мотивацию. "
            "Отвечай кратко, но с теплотой и уверенностью. Не пиши однотипно."
        )

        completion = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[{"role": "system", "content": system_prompt}, *conversation]
        )

        reply = completion.choices[0].message["content"]
        user_memory[user_id].append({"role": "assistant", "content": reply})
        await message.answer(reply)

    except Exception as e:
        await message.answer(f"⚠️ Ошибка: {e}")

async def main():
    print("🤖 Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

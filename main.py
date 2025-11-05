import openai
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message

# === Настройки ===
TELEGRAM_TOKEN = "ТВОЙ_ТЕЛЕГРАМ_ТОКЕН"
OPENAI_API_KEY = "ТВОЙ_OPENAI_API_KEY"

openai.api_key = OPENAI_API_KEY

TELEGRAM_TOKEN = os.getenv("BOT_TOKEN")
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

    user_memory[user_id].append({"role": "user", "content": message.text})
    conversation = user_memory[user_id]

    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Ты фитнес-тренер и психолог мотивации."},
                *conversation
            ]
        )

        reply = completion.choices[0].message["content"]
        user_memory[user_id].append({"role": "assistant", "content": reply})
        await message.answer(reply)

    except Exception as e:
        await message.answer("⚠️ Произошла ошибка: " + str(e))

async def main():
    print("🤖 Бот запущен...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

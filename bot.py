import os
import random
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
import asyncio
from dotenv import load_dotenv
from questions import QUESTIONS, CATEGORIES

load_dotenv()
BOT_TOKEN = os.getenv('8477738633:AAG0hYk0zo49_ANYl3tLqCPw6Kuzvl6B1m4')
WEBAPP_URL = "https://telegram-bot-9vk9.onrender.com"  # Замените на ваш URL

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

class QuestionStates(StatesGroup):
    waiting_category = State()

@dp.message(Command("start"))
async def start_handler(message: types.Message):
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Открыть Mini App", web_app=WebAppInfo(url=WEBAPP_URL))],
        *[ [InlineKeyboardButton(text=cat, callback_data=f"cat_{cat}")] for cat in CATEGORIES[:3] ],  # Первые 3 для примера
        [InlineKeyboardButton(text="Случайный вопрос", callback_data="random")]
    ])
    await message.answer(
        "Привет! Это бот для обсуждения вопросов. Выбери категорию или открой Mini App для интерактивного выбора.\n"
        "В групповом чате используй /question [категория] для генерации вопроса.",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data.startswith("cat_"))
async def category_callback(callback: types.CallbackQuery):
    cat = callback.data.split("_")[1]
    question = random.choice(QUESTIONS[cat])
    await callback.message.answer(f"Категория: {cat}\nВопрос: {question}")
    await callback.answer()

@dp.callback_query(lambda c: c.data == "random")
async def random_question(callback: types.CallbackQuery):
    all_questions = [q for cats in QUESTIONS.values() for q in cats]
    question = random.choice(all_questions)
    await callback.message.answer(f"Случайный вопрос: {question}")
    await callback.answer()

@dp.message(Command("question"))
async def question_handler(message: types.Message):
    args = message.text.split()[1:] if len(message.text.split()) > 1 else []
    if not args:
        await message.answer("Укажи категорию: /question дружба")
        return
    cat = args[0].lower().replace(" ", "_")
    if cat in QUESTIONS:
        question = random.choice(QUESTIONS[cat])
        await message.answer(f"Категория: {cat}\nВопрос для обсуждения: {question}")
    else:
        await message.answer(f"Неизвестная категория. Доступны: {', '.join(CATEGORIES)}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
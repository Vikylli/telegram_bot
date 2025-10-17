import os
from flask import Flask, request, jsonify, render_template
from aiogram import Bot
from aiogram.webhook import aiohttp_server
import asyncio
from dotenv import load_dotenv
from questions import QUESTIONS
import random

load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL', 'https://your-app.onrender.com/webhook')
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = int(os.getenv('PORT', 5000))

app = Flask(__name__)
bot = Bot(token=BOT_TOKEN)
dp = ...  # Импортируйте dp из bot.py или переместите логику

@app.route('/')
def index():
    return "Bot is running!"

@app.route('/miniapp')
def miniapp():
    return render_template('miniapp.html')  # Если templates/, иначе open('miniapp.html').read()

@app.route('/get_question')
def get_question():
    cat = request.args.get('cat', '').lower().replace(' ', '_')
    if cat in QUESTIONS:
        question = random.choice(QUESTIONS[cat])
        return jsonify({'question': f"Категория: {cat}\n{question}"})
    return jsonify({'error': 'Invalid category'}), 400

@app.route('/webhook', methods=['POST'])
async def webhook():
    # Для aiogram webhook: Используйте aiohttp или интегрируйте
    # Лучше: В bot.py используйте dp.start_webhook(...)
    # Пример настройки в main:
    # await bot.set_webhook(WEBHOOK_URL)
    # await aiohttp_server(dp, bot, host=WEBAPP_HOST, port=WEBAPP_PORT)
    update = request.json
    # Обработайте update вручную или используйте aiogram's webhook
    return 'OK'

if __name__ == '__main__':
    # Для локального теста: app.run()
    # Для webhook: настройте в bot.py
    app.run(host=WEBAPP_HOST, port=WEBAPP_PORT)
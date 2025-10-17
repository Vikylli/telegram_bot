from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import logging
import json

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

TOKEN = "8477738633:AAG0hYk0zo49_ANYl3tLqCPw6Kuzvl6B1m4"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Начать игру", web_app={"url": " https://telegram-bot-9vk9.onrender.com."})]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Привет! Нажми кнопку, чтобы начать игру и получить вопрос для обсуждения.", reply_markup=reply_markup)

# Обработка сообщений с данными от Web App
async def handle_webapp_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message and update.message.web_app_data:
        data = update.message.web_app_data.data
        try:
            parsed = json.loads(data)
            category = parsed.get('category', 'неизвестная тема')
            question = parsed.get('question', 'Вопрос не загрузился :(')
            
            await update.message.reply_text(
                f"Тема: *{category}*\n\nВопрос:\n{question}\n\nОбсудите его в чате!",
                parse_mode='Markdown'
            )
        except Exception as e:
            await update.message.reply_text(f"Ошибка при обработке данных: {e}")

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.StatusUpdate.WEB_APP_DATA, handle_webapp_data))

    application.run_polling()

if __name__ == '__main__':
    main()
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TELEGRAM_BOT_TOKEN = "7680132564:AAHUMhMhFY_QqSfHfqvA-Ja0m5p2RJBGe_I"
GEMINI_API_KEY = "AIzaSyDu7h5qYN-btiTrJX0Moy-tO6hagCVnXDg"
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=AIzaSyDu7h5qYN-btiTrJX0Moy-tO6hagCVnXDg" + GEMINI_API_KEY

BOT_ROLE = "Твоя задача - абсолютно без лишних слов, искать стихи Библии. Тебе дают запрос, мол найди такой-то стих, ты должен дать чёткий ответ, допустим Евангелие от Иоанна 2:12, и дальше следующим абзацем стих. Если стихов больше, то пропуская абзац, таким образом укажи и остальные. Не пиши ничего лишнего, только номер стиха и его текст"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Бот запущен.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text
    payload = {
        "contents": [{
            "role": "user",
            "parts": [{"text": f"{BOT_ROLE}\n{user_message}"}]
        }]
    }
    headers = {
        "Content-Type": "application/json"
    }
    response = requests.post(GEMINI_API_URL, json=payload, headers=headers)
    data = response.json()
    try:
        bot_reply = data['candidates'][0]['content']['parts'][0]['text']
    except (KeyError, IndexError):
        bot_reply = "Ошибка ответа от GeMini API."
    await update.message.reply_text(bot_reply)

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
app.run_polling()

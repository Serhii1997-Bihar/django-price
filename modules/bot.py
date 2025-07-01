import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pricesua_project.settings')

import django
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
django.setup()

from prices_app.models import PersonModel
from django.contrib.auth.models import User
from django.db.models.query import sync_to_async
import pricesua_project.settings

@sync_to_async
def get_registered_person(username):
    try:
        return PersonModel.objects.get(telegram=username)
    except PersonModel.DoesNotExist:
        return None

@sync_to_async
def update_chat_id(person, chat_id):
    person.chat_id = chat_id
    person.save()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    username = user.username
    chat_id = update.effective_chat.id

    if not username:
        await update.message.reply_text("❌ Тебе не знайдено в телеграмі, зареєструй свій username!")
        return

    person = await get_registered_person(username)

    if person:
        await update_chat_id(person, chat_id)
        await update.message.reply_text(f"✅ Вітаю, @{person.telegram}! Ти передав свій chat_id.")
    else:
        await update.message.reply_text("❌ Ти повинен зареєструвати свій username на сайті!")

if __name__ == "__main__":
    application = Application.builder().token(pricesua_project.settings.TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()

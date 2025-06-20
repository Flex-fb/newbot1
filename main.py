import os
import logging
from datetime import datetime
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
GROUP_ID = int(os.getenv("GROUP_ID"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    text = update.message.text or ""
    name = user.full_name or "Без имени"
    username = f"@{user.username}" if user.username else "—"
    user_id = user.id
    date = update.message.date.strftime("%Y-%m-%d %H:%M:%S")

    message = (
        f"<b>💬 Новое сообщение от клиента</b>

"
        f"<b>Имя:</b> {name}
"
        f"<b>Username:</b> {username}
"
        f"<b>Telegram ID:</b> <code>{user_id}</code>
"
        f"<b>Время:</b> {date}
"
        f"<b>Сообщение:</b> {text}
"
        f"<a href='tg://user?id={user_id}'>Ответить клиенту</a>"
    )

    # Пересылаем админу и в группу
    await context.bot.send_message(chat_id=ADMIN_ID, text=message, parse_mode="HTML")
    await context.bot.send_message(chat_id=GROUP_ID, text=message, parse_mode="HTML")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

import os
import logging
from datetime import datetime
from telegram import Update, ChatPermissions
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

TOKEN = os.environ.get("BOT_TOKEN")
GROUP_ID = int(os.environ.get("GROUP_ID"))
ADMIN_ID = int(os.environ.get("ADMIN_ID"))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    message = update.message.text or "<без текста>"
    now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Карточка клиента
    card = f"""<b>🧾 Новое сообщение от клиента</b>

👤 <b>Имя:</b> {user.first_name}
🔗 <b>Username:</b> @{user.username if user.username else 'нет'}
🆔 <b>ID:</b> <code>{user.id}</code>
🕒 <b>Время:</b> {now}
💬 <b>Сообщение:</b> {message}

🔁 <b>Ответить прямо здесь</b>
"""

    # Создать новый топик
    forum_topic = await context.bot.create_forum_topic(chat_id=GROUP_ID, name=f"{user.first_name} | @{user.username or 'нет'}")
    await context.bot.send_message(chat_id=GROUP_ID, message_thread_id=forum_topic.message_thread_id, text=card, parse_mode='HTML')

    # Переслать владельцу в личку
    await context.bot.send_message(chat_id=ADMIN_ID, text=card, parse_mode='HTML')


if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    app.run_polling()

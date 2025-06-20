import os
import logging
from datetime import datetime
from aiogram import Bot, Dispatcher, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor

API_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
GROUP_ID = int(os.getenv("GROUP_ID"))

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)

@dp.message_handler(content_types=types.ContentType.TEXT)
async def handle_message(message: types.Message):
    user = message.from_user
    full_name = user.full_name
    username = user.username or "не указан"
    user_id = user.id
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    text = message.text

    card = (
        f"<b>📩 Новое сообщение от клиента</b>\n\n"
        f"<b>👤 Имя:</b> {full_name}\n"
        f"<b>🔗 Username:</b> @{username}\n"
        f"<b>🆔 Telegram ID:</b> <code>{user_id}</code>\n"
        f"<b>⏰ Время:</b> {timestamp}\n"
        f"<b>💬 Сообщение:</b> {text}\n"
    )

    keyboard = InlineKeyboardMarkup().add(
        InlineKeyboardButton("✉️ Ответить", url=f"https://t.me/{username}")
    )

    # Отправка админу
    await bot.send_message(ADMIN_ID, card, reply_markup=keyboard)

    # Создание топика в группе
    forum_topic = await bot.create_forum_topic(
        chat_id=GROUP_ID,
        name=f"{full_name} (@{username})"
    )

    # Отправка карточки в созданный топик
    await bot.send_message(
        chat_id=GROUP_ID,
        message_thread_id=forum_topic.message_thread_id,
        text=card,
        reply_markup=keyboard
    )

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)

"""Обработчик команды /start, /new и /help."""

from telegram import Update
from telegram.ext import ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Приветственное сообщение и сброс диалога."""
    user = update.effective_user
    context.user_data.clear()

    await update.message.reply_text(
        f"👋 Привет, {user.first_name}!\n\n"
        "Я — твой **AI-психолог и бизнес-коуч** 🧠\n\n"
        "Помогаю предпринимателям:\n"
        "• 💬 Формулировать мысли для общения и переговоров\n"
        "• 🎯 Ставить и достигать цели\n"
        "• 🧱 Прорабатывать страхи и возражения\n"
        "• 💡 Развивать предпринимательское мышление\n\n"
        "Расскажи, что у тебя сейчас происходит. Чем могу помочь?",
    )

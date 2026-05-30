"""Обработчик команды /start и /new."""

from telegram import Update
from telegram.ext import ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Приветственное сообщение."""
    user = update.effective_user

    # Сбрасываем историю диалога при /start или /new
    if "history" in context.user_data:
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

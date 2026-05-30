"""Обработчик команды /new — сброс диалога."""

from telegram import Update
from telegram.ext import ContextTypes


async def new_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Сброс контекста диалога."""
    context.user_data.clear()

    await update.message.reply_text(
        "🔄 Диалог сброшен! Начинаем с чистого листа.\n\n"
        "Расскажи, что у тебя сейчас происходит — я помогу."
    )

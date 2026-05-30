"""Обработчик текстовых сообщений — основная логика диалога."""

import logging
from telegram import Update
from telegram.ext import ContextTypes

from src.prompts.system_prompt import COACH_SYSTEM_PROMPT
from config import MAX_HISTORY

logger = logging.getLogger(__name__)

TELEGRAM_MAX_LENGTH = 4096


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка входящего текстового сообщения."""
    if not update.message or not update.message.text:
        return

    user = update.effective_user
    text = update.message.text.strip()

    if not text:
        await update.message.reply_text("Напиши мне сообщение — я отвечу! 😊")
        return

    # ── Показываем индикатор печати ──
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing",
    )

    # ── Достаём AI-клиент ──
    ai_clients = context.application.bot_data.get("ai_clients", {})
    primary = context.application.bot_data.get("primary_ai", "gemini")
    ai = ai_clients.get(primary) or ai_clients.get("groq") or ai_clients.get("gemini")
    if not ai:
        await update.message.reply_text(
            "❌ AI не подключён. Попроси администратора настроить API ключ."
        )
        return

    # ── История диалога ──
    if "history" not in context.user_data:
        context.user_data["history"] = []

    history = context.user_data["history"]
    history.append({"role": "user", "parts": [text]})

    # Обрезаем историю до лимита (старые сообщения удаляются)
    trimmed_history = history[-MAX_HISTORY:]

    # ── Отправляем запрос к AI ──
    try:
        reply = await ai.chat(
            system_prompt=COACH_SYSTEM_PROMPT,
            history=trimmed_history,
        )

        history.append({"role": "model", "parts": [reply]})

        # ── Отправляем ответ (с разбивкой при превышении лимита) ──
        if len(reply) > TELEGRAM_MAX_LENGTH:
            chunks = []
            for i in range(0, len(reply), TELEGRAM_MAX_LENGTH):
                chunks.append(reply[i:i + TELEGRAM_MAX_LENGTH])

            for chunk in chunks:
                await update.message.reply_text(chunk)
        else:
            await update.message.reply_text(reply)

    except Exception as e:
        logger.error(f"AI error for user {user.id}: {e}", exc_info=True)
        await update.message.reply_text(
            "😔 Что-то пошло не так. Попробуй ещё раз или напиши /new чтобы начать заново."
        )

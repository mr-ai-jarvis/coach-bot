"""Обработчик текстовых сообщений — основная логика диалога."""

from telegram import Update
from telegram.ext import ContextTypes

from src.prompts.system_prompt import COACH_SYSTEM_PROMPT
from config import MAX_HISTORY

# Максимальная длина сообщения Telegram
TELEGRAM_MAX_LENGTH = 4096


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка входящего текстового сообщения."""
    user = update.effective_user
    text = update.message.text.strip()

    if not text:
        await update.message.reply_text("Напиши мне сообщение — я отвечу! 😊")
        return

    # ── Печатаем индикатор ──
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")

    # ── Достаём AI-клиент ──
    ai_clients = context.application.bot_data.get("ai_clients", {})
    ai = ai_clients.get("gemini") or ai_clients.get("groq")
    if not ai:
        await update.message.reply_text("❌ AI не подключён. Попроси администратора настроить API ключ.")
        return

    # ── История диалога ──
    if "history" not in context.user_data:
        context.user_data["history"] = []

    history = context.user_data["history"]
    history.append({"role": "user", "parts": [text]})

    # ── Отправляем запрос к AI ──
    try:
        reply = await ai.chat(
            system_prompt=COACH_SYSTEM_PROMPT,
            history=history[-MAX_HISTORY:],
        )

        history.append({"role": "model", "parts": [reply]})

        # ── Отправляем ответ (с разбивкой при превышении лимита) ──
        if len(reply) > TELEGRAM_MAX_LENGTH:
            for i in range(0, len(reply), TELEGRAM_MAX_LENGTH):
                chunk = reply[i:i + TELEGRAM_MAX_LENGTH]
                await update.message.reply_text(chunk)
        else:
            await update.message.reply_text(reply)

    except Exception as e:
        await update.message.reply_text(
            "😔 Что-то пошло не так. Попробуй ещё раз или напиши /new чтобы начать заново."
        )
        raise

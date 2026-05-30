"""Обработчик голосовых сообщений."""

import io
import logging
from telegram import Update
from telegram.ext import ContextTypes

from src.prompts.system_prompt import COACH_SYSTEM_PROMPT
from config import MAX_HISTORY

logger = logging.getLogger(__name__)

TELEGRAM_MAX_LENGTH = 4096


async def handle_voice(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка входящего голосового сообщения."""
    if not update.message or not update.message.voice:
        return

    user = update.effective_user
    voice = update.message.voice

    # ── Показываем индикатор ──
    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action="typing",
    )

    # ── Достаём AI-клиент ──
    ai_clients = context.application.bot_data.get("ai_clients", {})
    groq = ai_clients.get("groq")

    if not groq:
        await update.message.reply_text(
            "❌ Для голосовых сообщений нужен Groq API ключ с Whisper.\n"
            "Получить: https://console.groq.com"
        )
        return

    # ── Скачиваем аудио ──
    try:
        file = await context.bot.get_file(voice.file_id)
        audio_bytes = io.BytesIO()
        await file.download_to_memory(audio_bytes)
        audio_bytes.seek(0)
        raw_audio = audio_bytes.read()
        logger.info(f"Voice message from user {user.id}: {voice.duration}s, {len(raw_audio)} bytes")
    except Exception as e:
        logger.error(f"Failed to download voice: {e}", exc_info=True)
        await update.message.reply_text("😔 Не удалось загрузить голосовое сообщение. Попробуй ещё раз.")
        return

    # ── Распознаём речь через Groq Whisper ──
    try:
        transcript = await groq.transcribe_audio(raw_audio)
        if not transcript or not transcript.strip():
            await update.message.reply_text("🤔 Не удалось разобрать речь. Попробуй записать ещё раз, чётче.")
            return
    except Exception as e:
        logger.error(f"Whisper transcription failed: {e}", exc_info=True)
        await update.message.reply_text("😔 Ошибка распознавания речи. Попробуй ещё раз.")
        return

    # ── Показываем что распознали ──
    await update.message.reply_text(
        f"🎤 *Распознано:*\n{transcript.strip()}\n\n_Анализирую..._",
        parse_mode="Markdown",
    )

    # ── Отправляем транскрипт в AI для ответа ──
    # Приоритет: PRIMARY_AI → Groq (он же транскрибировал) → любой другой
    primary = context.application.bot_data.get("primary_ai", "groq")
    ai = ai_clients.get(primary) or groq or next(iter(ai_clients.values()), None)
    if not ai:
        await update.message.reply_text("❌ AI не подключён.")
        return

    if "history" not in context.user_data:
        context.user_data["history"] = []

    history = context.user_data["history"]
    history.append({"role": "user", "parts": [f"[Голосовое сообщение]: {transcript.strip()}"]})
    trimmed = history[-MAX_HISTORY:]

    try:
        reply = await ai.chat(
            system_prompt=COACH_SYSTEM_PROMPT,
            history=trimmed,
        )
        history.append({"role": "model", "parts": [reply]})

        if len(reply) > TELEGRAM_MAX_LENGTH:
            for i in range(0, len(reply), TELEGRAM_MAX_LENGTH):
                await update.message.reply_text(reply[i:i + TELEGRAM_MAX_LENGTH])
        else:
            await update.message.reply_text(reply)

    except Exception as e:
        logger.error(f"AI reply error (voice): {e}", exc_info=True)
        await update.message.reply_text("😔 Ошибка при ответе. Попробуй ещё раз.")

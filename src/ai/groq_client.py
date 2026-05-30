"""Клиент для Groq API — быстрый, бесплатный, без кредитной карты.

Поддерживает:
- Llama модели для текстовых ответов
- Whisper для распознавания голосовых сообщений
"""

import logging
from groq import AsyncGroq
from config import GROQ_MODEL

logger = logging.getLogger(__name__)


class GroqClient:
    """Обёртка над Groq API."""

    def __init__(self, api_key: str):
        self.client = AsyncGroq(api_key=api_key)
        self.model = GROQ_MODEL

    async def chat(self, system_prompt: str, history: list) -> str:
        """Отправить сообщение в Groq Llama и получить ответ."""
        messages = [{"role": "system", "content": system_prompt}]

        for msg in history:
            role = "user" if msg["role"] == "user" else "assistant"
            content = msg["parts"][0] if isinstance(msg["parts"], list) else msg["parts"]
            messages.append({"role": role, "content": content})

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.8,
                max_tokens=4096,
            )
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"Groq API error: {e}", exc_info=True)
            raise

    async def transcribe_audio(self, audio_bytes: bytes, filename: str = "voice.ogg") -> str:
        """Распознать голосовое сообщение через Groq Whisper."""
        try:
            response = await self.client.audio.transcriptions.create(
                file=(filename, audio_bytes),
                model="whisper-large-v3-turbo",
                language="ru",
                response_format="text",
            )
            return response
        except Exception as e:
            logger.error(f"Groq Whisper error: {e}", exc_info=True)
            raise

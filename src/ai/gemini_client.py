"""Клиент для Google Gemini API — бесплатный, без кредитной карты."""

import asyncio
import google.generativeai as genai
from config import GEMINI_MODEL


class GeminiClient:
    """Обёртка над Google Gemini API."""

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            model_name=GEMINI_MODEL,
            generation_config={
                "temperature": 0.8,
                "top_p": 0.95,
                "top_k": 40,
                "max_output_tokens": 4096,
            },
        )

    async def chat(self, system_prompt: str, history: list) -> str:
        """Отправить сообщение в Gemini и получить ответ."""
        # Gemini не поддерживает system_prompt напрямую —
        # добавляем его как первый контекстный поворот
        messages = [
            {"role": "user", "parts": [system_prompt + "\n\nЗапомни эти правила. Отвечай на русском."]},
            {"role": "model", "parts": ["Принято! Я буду следовать этим правилам и отвечать на русском."]},
        ]
        messages.extend(history)

        chat = self.model.start_chat(history=[])
        for msg in messages[:-1]:
            if msg["role"] == "user":
                await asyncio.to_thread(chat.send_message, msg["parts"][0])

        response = await asyncio.to_thread(chat.send_message, messages[-1]["parts"][0])
        return response.text

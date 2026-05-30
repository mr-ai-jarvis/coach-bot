"""Клиент для Groq API — быстрый, бесплатный, без кредитной карты."""

from groq import AsyncGroq
from config import GROQ_MODEL


class GroqClient:
    """Обёртка над Groq API (Llama модели)."""

    def __init__(self, api_key: str):
        self.client = AsyncGroq(api_key=api_key)
        self.model = GROQ_MODEL

    async def chat(self, system_prompt: str, history: list) -> str:
        """Отправить сообщение в Groq и получить ответ."""
        messages = [{"role": "system", "content": system_prompt}]

        for msg in history:
            role = "user" if msg["role"] == "user" else "assistant"
            messages.append({"role": role, "content": msg["parts"][0]})

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.8,
            max_tokens=4096,
        )

        return response.choices[0].message.content

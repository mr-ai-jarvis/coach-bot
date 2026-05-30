"""Настройки и конфигурация бота."""

import os

# Telegram
BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

# AI
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
GROQ_API_KEY = os.environ.get("GROQ_API_KEY", "")

# Какой AI использовать по умолчанию: "gemini" или "groq"
# Gemini — качественнее, Groq — быстрее
PRIMARY_AI = os.environ.get("PRIMARY_AI", "gemini")

# Модели
GEMINI_MODEL = "gemini-2.0-flash"  # Быстрая бесплатная модель
GROQ_MODEL = "llama-3.3-70b-versatile"

# Максимум сообщений в истории
MAX_HISTORY = 20

# OpenAI-совместимость (если потребуется)
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "")
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

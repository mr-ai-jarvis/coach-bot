"""
Coach Bot — главный entry point.
Запускает Telegram бота с AI-коучем для предпринимателей.
"""

import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, MessageHandler, CommandHandler, filters

from src.handlers.start import start_command
from src.handlers.new import new_command
from src.handlers.help import help_command
from src.handlers.messages import handle_message
from src.ai.gemini_client import GeminiClient
from src.ai.groq_client import GroqClient
from src.web.health import start_health_server

load_dotenv()

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)


def main() -> None:
    """Запуск бота."""
    bot_token = os.environ.get("BOT_TOKEN")
    if not bot_token:
        logger.error("❌ BOT_TOKEN не задан!")
        return

    # Инициализация AI-клиентов
    gemini_key = os.environ.get("GEMINI_API_KEY")
    groq_key = os.environ.get("GROQ_API_KEY")

    if not gemini_key and not groq_key:
        logger.error("❌ Нужен хотя бы один AI API ключ (GEMINI_API_KEY или GROQ_API_KEY)!")
        return

    ai_clients = {}
    if gemini_key:
        ai_clients["gemini"] = GeminiClient(gemini_key)
        logger.info("✅ Gemini AI подключён")
    if groq_key:
        ai_clients["groq"] = GroqClient(groq_key)
        logger.info("✅ Groq AI подключён")

    # Telegram App
    app = Application.builder().token(bot_token).build()
    app.bot_data["ai_clients"] = ai_clients
    app.bot_data["primary_ai"] = os.environ.get("PRIMARY_AI", "gemini")

    # Регистрируем хендлеры
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("new", new_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Запускаем health-сервер для Railway (проверяет, что бот жив)
    start_health_server()

    logger.info("🧠 Coach Bot запущен...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()

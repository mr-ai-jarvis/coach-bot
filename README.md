# 🧠 Coach Bot — AI-психолог для предпринимателей

Telegram-бот на базе Google Gemini API. Помогает в общении, развивает предпринимательское мышление, мотивирует и ведёт к результатам.

## Возможности

- 🗣 **Коуч по общению** — помогает формулировать мысли, вести переговоры
- 💼 **Предпринимательский наставник** — развивает мышление, даёт советы
- 🎯 **Постановка целей** — помогает структурировать задачи
- 🔄 **История диалогов** — помнит контекст беседы
- 🎤 **Голосовые сообщения** — распознаёт речь через Groq Whisper
- 🚀 **Бесплатно** — работает на Google Gemini + Groq API

## Деплой на Railway

[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/template/...)

## Быстрый старт

```bash
git clone https://github.com/mr-ai-jarvis/coach-bot.git
cd coach-bot
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
# Отредактируй .env — вставь свои токены
python bot.py
```

## Переменные окружения

| Переменная | Описание |
|-----------|----------|
| `BOT_TOKEN` | Токен Telegram бота (получить у [@BotFather](https://t.me/BotFather)) |
| `GEMINI_API_KEY` | Ключ Google Gemini API ([получить бесплатно](https://aistudio.google.com/apikey)) |
| `GROQ_API_KEY` | (Опционально) Ключ Groq для быстрых ответов |

## Получение бесплатных API-ключей

### Google Gemini API (рекомендуется)
1. Перейди на [Google AI Studio](https://aistudio.google.com/apikey)
2. Нажми "Get API Key"
3. Выбери "Create API Key"
4. Скопируй ключ — готово! 1500 запросов/день бесплатно, без кредитной карты.

### Groq API (опционально, для скорости)
1. Перейди на [console.groq.com](https://console.groq.com)
2. Зарегистрируйся
3. Получи бесплатный API ключ (14 000 запросов/день)

### Telegram Bot Token
1. Напиши [@BotFather](https://t.me/BotFather) в Telegram
2. Отправь `/newbot` и следуй инструкциям
3. Скопируй полученный токен

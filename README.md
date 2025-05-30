# 🌦 Telegram Weather Bot

Простой Telegram-бот на Python с выбором языка (русский 🇷🇺 и английский eng), который показывает текущую погоду по введённому городу, используя OpenWeather API.

## 🛠 Используемые технологии

- Python 3.10+
- aiogram 3.x
- aiohttp
- python-dotenv
- OpenWeather API

## ⚙️ Как запустить

1. Склонируйте репозиторий:

```bash
git clone https://github.com/your-username/telegram-weather-bot.git
cd telegram-weather-bot
```

2. Установите зависимости:

```bash
pip install -r requirements.txt
```

3. Создайте `.env` файл на основе `.env.example`:

```env
BOT_TOKEN=ваш_токен_бота
WEATHER_API=ваш_ключ_погоды
```

4. Запустите бота:

```bash
python bot.py
```

##  Зависимости

```bash
pip freeze > requirements.txt
```

##  Пример взаимодействия

- `/start` — выбор языка
- После выбора языка — введите название города


# telegram-weather-bot

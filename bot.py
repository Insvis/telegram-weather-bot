import os
import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery, BotCommand
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API = os.getenv("WEATHER_API")

user_languages = {}

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)
router = Router()
dp.include_router(router)

async def get_weather(city: str, lang: str):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={WEATHER_API}&units=metric&lang={lang}"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                if lang == "eng":
                    return "City not found. Please try again."
                return "Город не найден. Попробуй снова."
            data = await resp.json()
            temp = data["main"]["temp"]
            desc = data["weather"][0]["description"]
            if lang == "eng":
                return f"Temperature: {temp}°C\n☁️ Condition: {desc.capitalize()}"
            return f"Температура: {temp}°C\n☁️ Состояние: {desc.capitalize()}"

start_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Русский", callback_data="lang_ru")],
        [InlineKeyboardButton(text="English", callback_data="lang_eng")]
    ]
)

@router.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я могу показать тебе погоду.\nHi! I can show you the weather.",
        reply_markup=start_keyboard
    )

@router.message()
async def handle_city(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name
    city = message.text.strip()
    print(f'{user_id},  {username}, {first_name},--->{city}<---')
    lang = user_languages.get(user_id, "ru")
    weather = await get_weather(city, lang)
    await message.answer(weather)

@router.callback_query(F.data == "lang_ru")
async def handle_start_button(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_languages[user_id] = "ru"
    await callback.message.answer("Напиши название города, чтобы узнать погоду ☁️")
    await callback.answer()

@router.callback_query(F.data == "lang_eng")
async def handle_start_button(callback: CallbackQuery):
    user_id = callback.from_user.id
    user_languages[user_id] = "eng"
    await callback.message.answer("Write down the name of the city to find out the weather☁️")
    await callback.answer()

async def main():
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
    ])
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())

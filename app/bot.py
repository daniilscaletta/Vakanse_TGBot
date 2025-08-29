import asyncio
import aiohttp
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from typing import List
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from app.models import Vacancy
from app.config import config

# Валидируем конфигурацию при импорте
config.validate()

# Инициализация бота и диспетчера
bot = Bot(token=config.BOT_TOKEN)
dp = Dispatcher()

# Инициализация планировщика
scheduler = AsyncIOScheduler()

async def get_vacancies_from_api() -> List[Vacancy]:
    try:
        api_url = f"http://{config.API_HOST}:{config.API_PORT}/vacancies"
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    return [Vacancy(**vacancy) for vacancy in data]
                else:
                    print(f"API вернул статус {response.status}")
                    return []
    except Exception as e:
        print(f"Ошибка при получении вакансий из API: {e}")
        return []

def format_vacancy_message(vacancy: Vacancy) -> str:
    """
    Форматирует вакансию для отображения в Telegram
    """
    return (
        f"🏢 <b>{vacancy.title}</b>\n"
        f"💰 <b>Зарплата:</b> {vacancy.salary}\n"
        f"🔗 <a href='{vacancy.url}'>Открыть вакансию</a>\n"
        f"{'─' * 34}"
    )

async def send_daily_vacancies():
    if not config.NOTIFICATION_USER_ID:
        print("❌ ID пользователя для уведомлений не установлен")
        return
    
    try:
        print("🕕 Отправка ежедневных вакансий...")
        
        vacancies = await get_vacancies_from_api()
        
        if not vacancies:
            await bot.send_message(
                config.NOTIFICATION_USER_ID,
                "❌ К сожалению, не удалось получить вакансии. Попробуйте позже."
            )
            return
        
        # Отправляем заголовок
        await bot.send_message(
            config.NOTIFICATION_USER_ID,
            f"🌅 Доброе утро! Найдено {len(vacancies)} новых вакансий:\n\n"
            "Вот актуальные предложения для Вас:"
        )
        
        batch_size = 5
        for i in range(0, len(vacancies), batch_size):
            batch = vacancies[i:i + batch_size]
            message_text = "\n\n".join([format_vacancy_message(vac) for vac in batch])
            
            await bot.send_message(
                config.NOTIFICATION_USER_ID,
                message_text,
                parse_mode="HTML",
                disable_web_page_preview=True
            )
            
            # Небольшая пауза между сообщениями
            if i + batch_size < len(vacancies):
                await asyncio.sleep(1)
        
        await bot.send_message(
            config.NOTIFICATION_USER_ID,
            "✅ Ежедневные вакансии загружены! Используйте /start для обновления списка."
        )
        
        print("✅ Ежедневные вакансии отправлены успешно")
        
    except Exception as e:
        print(f"❌ Ошибка при отправке ежедневных вакансий: {e}")
        try:
            await bot.send_message(
                config.NOTIFICATION_USER_ID,
                "❌ Произошла ошибка при получении ежедневных вакансий."
            )
        except:
            pass

@dp.message(Command("start"))
async def cmd_start(message: Message):
    # Сохраняем ID пользователя для автоматических уведомлений
    if not config.NOTIFICATION_USER_ID:
        config.NOTIFICATION_USER_ID = message.from_user.id
        print(f"👤 Установлен ID пользователя для уведомлений: {config.NOTIFICATION_USER_ID}")
    
    await message.answer("🔍 Ищу актуальные вакансии из Pentest, DevOps, Develop...")
    
    try:
        vacancies = await get_vacancies_from_api()
        
        if not vacancies:
            await message.answer("❌ К сожалению, не удалось получить вакансии. Попробуйте позже.")
            return
        
        await message.answer(
            f"📋 Найдено {len(vacancies)} вакансий:\n\n"
            "Вот актуальные предложения для Вас:"
        )
        
        batch_size = 5
        for i in range(0, len(vacancies), batch_size):
            batch = vacancies[i:i + batch_size]
            message_text = "\n\n".join([format_vacancy_message(vac) for vac in batch])
            
            await message.answer(
                message_text,
                parse_mode="HTML",
                disable_web_page_preview=True
            )
            
            if i + batch_size < len(vacancies):
                await asyncio.sleep(1)
        
        await message.answer(
            "✅ Все вакансии загружены! Используйте /start для обновления списка.\n\n"
            "🤖 Бот будет автоматически отправлять новые вакансии каждый день в 6:00!\n\n"
        )
        
    except Exception as e:
        print(f"Ошибка в обработчике start: {e}")
        await message.answer(
            "❌ Произошла ошибка при получении вакансий. Попробуйте позже."
        )

@dp.message()
async def echo_message(message: Message):
    await message.answer(
        "👋 Привет! Я бот для поиска вакансий Python разработчика.\n\n"
        "Используйте команду /start для получения актуальных вакансий.\n\n"
        "🤖 Бот будет автоматически отправлять новые вакансии каждый день в 6:00!\n\n"
    )

def setup_scheduler():
    # Добавляем задачу на отправку вакансий каждый день в 6:00
    scheduler.add_job(
        send_daily_vacancies,
        CronTrigger(hour=6, minute=0),
        id="daily_vacancies",
        name="Отправка ежедневных вакансий",
        replace_existing=True
    )
    
    print("⏰ Планировщик настроен: вакансии будут отправляться каждый день в 6:00")

async def main():
    print("🤖 Запуск Telegram бота...")
    
    setup_scheduler()
    
    # Запускаем планировщик
    scheduler.start()
    print("✅ Планировщик запущен")
    
    try:
        # Запускаем бота
        await dp.start_polling(bot)
    finally:
        # Останавливаем планировщик при завершении
        scheduler.shutdown()
        print("🛑 Планировщик остановлен")

if __name__ == "__main__":
    asyncio.run(main())

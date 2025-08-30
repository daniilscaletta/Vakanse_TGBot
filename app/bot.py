import asyncio
import logging
from typing import List

import aiohttp
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from apscheduler import events

from app.config import config
from app.models import Vacancy

PLANNING_HOUR = 6
PLANNING_MINUTE = 0

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('logs/bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Валидируем конфигурацию при импорте
config.validate()

# Инициализация бота и диспетчера
bot = Bot(token=config.BOT_TOKEN or "")
dp = Dispatcher()

# Инициализация планировщика
scheduler = AsyncIOScheduler()


async def get_vacancies_from_api() -> List[Vacancy]:
    try:
        api_url = f"http://{config.API_HOST}:{config.API_PORT}/vacancies"
        logger.info(f"Запрос к API: {api_url}")
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status == 200:
                    data = await response.json()
                    logger.info(f"Получено {len(data)} вакансий из API")
                    return [Vacancy(**vacancy) for vacancy in data]
                else:
                    logger.error(f"API вернул статус {response.status}")
                    return []
    except Exception as e:
        logger.error(f"Ошибка при получении вакансий из API: {e}")
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


async def send_daily_vacancies() -> None:
    if not config.NOTIFICATION_USER_ID:
        logger.error("❌ ID пользователя для уведомлений не установлен")
        return

    try:
        logger.info("🕕 Отправка ежедневных вакансий...")

        vacancies = await get_vacancies_from_api()

        if not vacancies:
            await bot.send_message(
                config.NOTIFICATION_USER_ID,
                "❌ К сожалению, не удалось получить вакансии. Попробуйте позже.",
            )
            return

        # Отправляем заголовок
        await bot.send_message(
            config.NOTIFICATION_USER_ID,
            f"🌅 Доброе утро! Найдено {len(vacancies)} новых вакансий:\n\n"
            "Вот актуальные предложения для Вас:",
        )

        batch_size = 5
        for i in range(0, len(vacancies), batch_size):
            batch = vacancies[i : i + batch_size]
            message_text = "\n\n".join([format_vacancy_message(vac) for vac in batch])

            await bot.send_message(
                config.NOTIFICATION_USER_ID,
                message_text,
                parse_mode="HTML",
                disable_web_page_preview=True,
            )

            # Небольшая пауза между сообщениями
            if i + batch_size < len(vacancies):
                await asyncio.sleep(1)

        await bot.send_message(
            config.NOTIFICATION_USER_ID,
            "✅ Ежедневные вакансии загружены! Используйте /start для "
            "обновления списка.",
        )

        logger.info("✅ Ежедневные вакансии отправлены успешно")

    except Exception as e:
        logger.error(f"❌ Ошибка при отправке ежедневных вакансий: {e}")
        try:
            await bot.send_message(
                config.NOTIFICATION_USER_ID,
                "❌ Произошла ошибка при получении ежедневных вакансий.",
            )
        except Exception:
            pass


@dp.message(Command("start"))
async def cmd_start(message: Message) -> None:
    # Сохраняем ID пользователя для автоматических уведомлений
    if not config.NOTIFICATION_USER_ID:
        if message.from_user:
            config.NOTIFICATION_USER_ID = str(message.from_user.id)
        print(
            f"👤 Установлен ID пользователя для уведомлений: "
            f"{config.NOTIFICATION_USER_ID}"
        )

    await message.answer("🔍 Ищу актуальные вакансии из Pentest, DevOps, Develop...")

    try:
        vacancies = await get_vacancies_from_api()

        if not vacancies:
            await message.answer(
                "❌ К сожалению, не удалось получить вакансии. Попробуйте позже."
            )
            return

        await message.answer(
            f"📋 Найдено {len(vacancies)} вакансий:\n\n"
            "Вот актуальные предложения для Вас:"
        )

        batch_size = 5
        for i in range(0, len(vacancies), batch_size):
            batch = vacancies[i : i + batch_size]
            message_text = "\n\n".join([format_vacancy_message(vac) for vac in batch])

            await message.answer(
                message_text, parse_mode="HTML", disable_web_page_preview=True
            )

            if i + batch_size < len(vacancies):
                await asyncio.sleep(1)

        await message.answer(
            "✅ Все вакансии загружены! Используйте /start для обновления списка.\n\n"
            "🤖 Бот будет автоматически отправлять новые вакансии каждый день в "
            "6:00!\n\n"
        )

    except Exception as e:
        print(f"Ошибка в обработчике start: {e}")
        await message.answer(
            "❌ Произошла ошибка при получении вакансий. Попробуйте позже."
        )


@dp.message()
async def echo_message(message: Message) -> None:
    await message.answer(
        "👋 Привет! Я бот для поиска вакансий Python разработчика.\n\n"
        "Используйте команду /start для получения актуальных вакансий.\n\n"
        "🤖 Бот будет автоматически отправлять новые вакансии каждый день в "
        "6:00!\n\n"
    )


def setup_scheduler() -> None:
    # Добавляем задачу на отправку вакансий каждый день в 6:00
    job = scheduler.add_job(
        send_daily_vacancies,
        CronTrigger(hour=PLANNING_HOUR-3, minute=PLANNING_MINUTE),
        id="daily_vacancies",
        name="Отправка ежедневных вакансий",
        replace_existing=True,
    )

    logger.info(f"⏰ Планировщик настроен: вакансии будут отправляться каждый день в 6:00")
    logger.info(f"📅 Следующий запуск задачи: {job.next_run_time if hasattr(job, 'next_run_time') else 'Не определено'}")
    
    # Добавляем обработчик ошибок планировщика
    def job_error_listener(event):
        logger.error(f"❌ Ошибка в задаче планировщика: {event.exception}")
        logger.error(f"   Задача: {event.job_id}")
        logger.error(f"   Детали: {event.traceback}")

    scheduler.add_listener(job_error_listener, events.EVENT_JOB_ERROR)
    logger.info("🔧 Добавлен обработчик ошибок планировщика")


async def main() -> None:
    logger.info("🤖 Запуск Telegram бота...")
    logger.info(f"🔧 Конфигурация: API_HOST={config.API_HOST}, API_PORT={config.API_PORT}")
    logger.info(f"👤 USER_ID для уведомлений: {config.NOTIFICATION_USER_ID}")

    setup_scheduler()

    # Запускаем планировщик
    scheduler.start()
    logger.info("✅ Планировщик запущен")
    
    # Выводим информацию о запланированных задачах
    jobs = scheduler.get_jobs()
    logger.info(f"📋 Активных задач в планировщике: {len(jobs)}")
    for job in jobs:
        next_run = job.next_run_time if hasattr(job, 'next_run_time') else 'Не определено'
        logger.info(f"  - {job.name} (ID: {job.id}): {next_run}")

    try:
        # Запускаем бота
        await dp.start_polling(bot)
    finally:
        # Останавливаем планировщик при завершении
        scheduler.shutdown()
        logger.info("🛑 Планировщик остановлен")


if __name__ == "__main__":
    asyncio.run(main())

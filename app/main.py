import asyncio

import uvicorn
from fastapi import FastAPI

from app.bot import bot, dp, scheduler, setup_scheduler
from app.config import config
from app.models import Vacancy
from app.parser import get_top_vacancies

app = FastAPI()


@app.get("/health", summary="CHECK")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/vacancies", response_model=list[Vacancy])
def vacancies() -> list[Vacancy]:
    result = get_top_vacancies()
    return result or []


async def run_bot() -> None:
    print("🤖 Запуск Telegram бота...")
    await dp.start_polling(bot)


async def run_api() -> None:
    uvicorn_config = uvicorn.Config(app, host=config.API_HOST, port=config.API_PORT)
    server = uvicorn.Server(uvicorn_config)
    await server.serve()


async def run_scheduler() -> None:
    print("📅 Запуск планировщика задач...")

    setup_scheduler()
    scheduler.start()
    print("✅ Планировщик запущен")

    try:
        while True:
            await asyncio.sleep(1)
    except KeyboardInterrupt:
        scheduler.shutdown()


async def main() -> None:
    print("🚀 Запуск приложения...")
    print(f"📡 API будет доступен на http://{config.API_HOST}:{config.API_PORT}")
    print("🤖 Telegram бот запускается...")
    print("📅 Планировщик задач запускается...")

    await asyncio.gather(run_api(), run_bot(), run_scheduler())


if __name__ == "__main__":
    asyncio.run(main())

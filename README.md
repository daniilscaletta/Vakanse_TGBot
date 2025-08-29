# Vakanse Telegram Bot

Telegram бот для поиска и автоматической отправки вакансий Python разработчика.

## Возможности

- 🔍 Поиск актуальных вакансий Python разработчика
- 🤖 Автоматическая отправка вакансий каждый день в 6:00
- 📡 REST API для получения вакансий
- 🧪 Тестирование автоматической отправки

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone <repository-url>
cd Vakanse_TGBot
```

2. Создайте виртуальное окружение и установите зависимости:
```bash
python -m venv venv
source venv/bin/activate  # На Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. Создайте файл `.env` с настройками:
```env
BOT_TOKEN=your_telegram_bot_token_here
HOST=0.0.0.0
PORT=8000
MAX_VACANCIES=20
```

4. Запустите приложение:
```bash
python -m app.main
```

## Использование

### Telegram Bot

1. Найдите бота в Telegram и отправьте команду `/start`
2. Бот автоматически сохранит ваш ID для ежедневных уведомлений

### API

- `GET /health` - проверка состояния сервиса
- `GET /vacancies` - получение списка вакансий

## Автоматическая отправка

Бот автоматически отправляет вакансии каждый день в 6:00 утра. Для этого:

1. Отправьте команду `/start` боту (это сохранит ваш ID)
2. Бот будет отправлять вакансии автоматически
3. Используйте `/test_daily` для тестирования

## Структура проекта

```
Vakanse_TGBot/
├── app/
│   ├── bot.py          # Telegram бот с планировщиком
│   ├── config.py       # Конфигурация
│   ├── main.py         # Основное приложение
│   ├── models.py       # Модели данных
│   └── parser.py       # Парсер вакансий
├── requirements.txt    # Зависимости
└── README.md          # Документация
```

## Технологии

- Python 3.13+
- aiogram 3.22.0 (Telegram Bot API)
- FastAPI (REST API)
- APScheduler (планировщик задач)
- BeautifulSoup4 (парсинг)
- aiohttp (HTTP клиент)

## Лицензия

MIT

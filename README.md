# Vakanse Telegram Bot

Telegram бот для поиска и автоматической отправки вакансий Python разработчика.

## 🚀 Возможности

- 🔍 Поиск актуальных вакансий Python разработчика
- 🤖 Автоматическая отправка вакансий каждый день в 6:00
- 📡 REST API для получения вакансий
- 🧪 Тестирование автоматической отправки
- 🐳 Docker контейнеризация
- 🔧 Pre-commit hooks для качества кода
- 📊 Покрытие тестами
- 🏗️ CI/CD готовность

## 📋 Требования

- Python 3.9+
- Docker & Docker Compose (для продакшена)
- Telegram Bot Token (от @BotFather)

## 🛠️ Быстрый старт

### Вариант 1: Docker (Рекомендуется для продакшена)

1. **Клонируйте репозиторий:**

```bash
git clone <repository-url>
cd Vakanse_TGBot
```

2. **Настройте переменные окружения:**

```bash
cp env.example .env
# Отредактируйте .env файл с вашими настройками
```

3. **Запустите с одной кнопки:**

```bash
chmod +x scripts/start.sh
./scripts/start.sh
```

### Вариант 2: Локальная разработка

1. **Настройте среду разработки:**

```bash
make dev-setup
# или
./scripts/dev-setup.sh
```

2. **Запустите приложение:**

```bash
python -m app.main
```

## 🐳 Docker команды

```bash
# Запуск приложения
make docker-run
# или
./scripts/start.sh

# Просмотр логов
make docker-logs
# или
./scripts/start.sh logs

# Остановка
make docker-stop
# или
./scripts/start.sh stop

# Перезапуск
make docker-restart
# или
./scripts/start.sh restart

# Проверка статуса
make status
# или
./scripts/start.sh status
```

## 🔧 Разработка

### Настройка среды разработки

```bash
# Полная настройка
make dev-setup

# Или пошагово:
make install          # Установка зависимостей
make pre-commit       # Настройка pre-commit hooks
make format           # Форматирование кода
make lint             # Линтинг
make test             # Запуск тестов
```

### Команды разработки

```bash
# Форматирование кода
make format

# Линтинг
make lint

# Тесты
make test
make test-html        # С HTML отчетом

# Pre-commit hooks
make pre-commit

# Очистка
make clean
```

### Структура проекта

```
Vakanse_TGBot/
├── app/                    # Основной код приложения
│   ├── __init__.py
│   ├── bot.py             # Telegram бот
│   ├── config.py          # Конфигурация
│   ├── main.py            # Точка входа
│   ├── models.py          # Модели данных
│   └── parser.py          # Парсер вакансий
├── tests/                 # Тесты
│   ├── __init__.py
│   ├── test_config.py
│   └── test_models.py
├── scripts/               # Скрипты запуска
│   ├── start.sh          # Основной скрипт запуска
│   └── dev-setup.sh      # Настройка разработки
├── logs/                  # Логи (создается автоматически)
├── .env                   # Переменные окружения
├── env.example           # Пример .env файла
├── requirements.txt      # Зависимости продакшена
├── requirements-dev.txt  # Зависимости разработки
├── pyproject.toml       # Конфигурация инструментов
├── Dockerfile           # Docker образ
├── docker-compose.yml   # Docker Compose
├── Makefile             # Команды разработки
├── .pre-commit-config.yaml  # Pre-commit hooks
├── .flake8              # Конфигурация flake8
└── README.md            # Документация
```

## ⚙️ Конфигурация

### Переменные окружения

Создайте файл `.env` на основе `env.example`:

```env
# Telegram Bot Configuration
BOT_TOKEN=your_bot_token_here
USER_ID=your_telegram_user_id_here

# API Configuration
HOST=0.0.0.0
PORT=8000

# Application Configuration
MAX_VACANCIES=20
LOG_LEVEL=INFO
```

### Получение Telegram Bot Token

1. Найдите @BotFather в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям для создания бота
4. Скопируйте полученный токен в `.env` файл

## 📡 API Endpoints

- `GET /health` - Проверка состояния сервиса
- `GET /vacancies` - Получение списка вакансий

## 🧪 Тестирование

```bash
# Запуск всех тестов
make test

# Запуск с покрытием
make test-html

# Запуск конкретного теста
pytest tests/test_config.py -v
```

## 🔍 Мониторинг

### Health Check

```bash
curl http://localhost:8000/health
```

### Логи

```bash
# Docker логи
make docker-logs

# Локальные логи
tail -f logs/app.log
```

## 🚀 Деплой

### Docker Compose (Рекомендуется)

```bash
# Продакшен деплой
make prod

# Или пошагово:
make env-check
make docker-build
make docker-run
```

### Docker без Compose

```bash
# Сборка образа
make prod-build

# Запуск контейнера
make prod-run

# Остановка
make prod-stop
```

## 🔒 Безопасность

- ✅ Не запускается от root пользователя
- ✅ Health checks для мониторинга
- ✅ Переменные окружения для секретов
- ✅ Docker security best practices
- ✅ Pre-commit hooks для качества кода

## 📊 Качество кода

Проект использует современные инструменты для обеспечения качества кода:

- **Black** - Форматирование кода
- **isort** - Сортировка импортов
- **flake8** - Линтинг
- **mypy** - Статическая типизация
- **pre-commit** - Автоматические проверки
- **pytest** - Тестирование
- **coverage** - Покрытие тестами

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Запустите тесты: `make test`
5. Отформатируйте код: `make format`
6. Создайте Pull Request

## 📝 Лицензия

MIT License

## 🆘 Поддержка

Если у вас возникли проблемы:

1. Проверьте логи: `make docker-logs`
2. Проверьте статус: `make status`
3. Проверьте конфигурацию: `make env-check`
4. Создайте Issue в репозитории

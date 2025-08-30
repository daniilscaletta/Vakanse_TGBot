#!/bin/bash

# Скрипт для управления Telegram ботом вакансий

BOT_PID_FILE="bot.pid"
LOG_FILE="logs/bot.log"

case "$1" in
    start)
        echo "🤖 Запуск бота..."
        if [ -f "$BOT_PID_FILE" ]; then
            echo "❌ Бот уже запущен (PID: $(cat $BOT_PID_FILE))"
            exit 1
        fi
        
        # Активируем виртуальное окружение и запускаем бота
        source venv/bin/activate
        nohup python -m app.bot > bot_output.log 2>&1 &
        echo $! > "$BOT_PID_FILE"
        echo "✅ Бот запущен (PID: $(cat $BOT_PID_FILE))"
        echo "📋 Логи: tail -f $LOG_FILE"
        ;;
        
    stop)
        echo "🛑 Остановка бота..."
        if [ -f "$BOT_PID_FILE" ]; then
            PID=$(cat "$BOT_PID_FILE")
            if kill -0 "$PID" 2>/dev/null; then
                kill "$PID"
                rm -f "$BOT_PID_FILE"
                echo "✅ Бот остановлен"
            else
                echo "❌ Процесс бота не найден"
                rm -f "$BOT_PID_FILE"
            fi
        else
            echo "❌ Файл PID не найден"
        fi
        ;;
        
    restart)
        echo "🔄 Перезапуск бота..."
        $0 stop
        sleep 2
        $0 start
        ;;
        
    status)
        if [ -f "$BOT_PID_FILE" ]; then
            PID=$(cat "$BOT_PID_FILE")
            if kill -0 "$PID" 2>/dev/null; then
                echo "✅ Бот запущен (PID: $PID)"
                echo "📋 Последние логи:"
                tail -5 "$LOG_FILE" 2>/dev/null || echo "   Логи не найдены"
            else
                echo "❌ Бот не запущен (PID файл устарел)"
                rm -f "$BOT_PID_FILE"
            fi
        else
            echo "❌ Бот не запущен"
        fi
        ;;
        
    logs)
        if [ -f "$LOG_FILE" ]; then
            tail -f "$LOG_FILE"
        else
            echo "❌ Файл логов не найден: $LOG_FILE"
        fi
        ;;
        
    test)
        echo "🧪 Тестирование функций бота..."
        source venv/bin/activate
        python test_vacancies.py
        ;;
        
    *)
        echo "Использование: $0 {start|stop|restart|status|logs|test}"
        echo ""
        echo "Команды:"
        echo "  start   - Запустить бота"
        echo "  stop    - Остановить бота"
        echo "  restart - Перезапустить бота"
        echo "  status  - Показать статус бота"
        echo "  logs    - Показать логи в реальном времени"
        echo "  test    - Запустить тесты"
        exit 1
        ;;
esac

#!/bin/bash

# Скрипт запуска Telegram бота

# Получаем директорию скрипта
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# Проверка наличия виртуального окружения
if [ ! -d "venv" ]; then
    echo "Ошибка: виртуальное окружение не найдено!"
    echo "Создайте его командой: python3 -m venv venv"
    exit 1
fi

# Проверка наличия .env файла
if [ ! -f ".env" ]; then
    echo "Ошибка: файл .env не найден!"
    echo "Создайте его из примера: cp .env.example .env"
    exit 1
fi

# Активация виртуального окружения и запуск бота
source venv/bin/activate
exec python bot.py

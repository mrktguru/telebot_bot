# Инструкция по деплою бота на сервер

## Быстрый старт

Подключитесь к серверу и выполните команды:

```bash
ssh root@38.244.194.181
```

## Вариант 1: Автоматическая установка (Рекомендуется)

Скопируйте и выполните этот скрипт одной командой:

```bash
cd /telebot && \
git clone https://github.com/Mrktguru/telebot_bot.git . 2>/dev/null || git pull origin main && \
apt update && apt install -y python3 python3-pip python3-venv && \
python3 -m venv venv && \
source venv/bin/activate && \
pip install -r requirements.txt && \
chmod +x start.sh && \
echo "Теперь создайте файл .env с вашим токеном бота"
```

После выполнения команды:

1. Создайте файл `.env`:
```bash
nano .env
```

2. Вставьте эти строки и замените `YOUR_BOT_TOKEN` на ваш токен от @BotFather:
```
BOT_TOKEN=YOUR_BOT_TOKEN
WELCOME_IMAGE=images/welcome.jpg
```

3. Загрузите изображение (опционально):
```bash
# Создайте папку images если её нет
mkdir -p images

# Загрузите ваше изображение через scp с локального компьютера
# scp /path/to/your/image.jpg root@38.244.194.181:/telebot/images/welcome.jpg

# Или скачайте из интернета
# wget -O images/welcome.jpg URL_вашего_изображения
```

4. Настройте автозапуск:
```bash
cp telebot.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable telebot
systemctl start telebot
systemctl status telebot
```

## Вариант 2: Пошаговая установка

### Шаг 1: Подготовка директории

```bash
cd /telebot
```

### Шаг 2: Клонирование репозитория

Если директория пустая:
```bash
git clone https://github.com/Mrktguru/telebot_bot.git .
```

Если уже клонирован, обновите:
```bash
git pull origin main
```

### Шаг 3: Установка Python и зависимостей

```bash
# Обновить пакеты
apt update

# Установить Python и pip
apt install -y python3 python3-pip python3-venv

# Создать виртуальное окружение
python3 -m venv venv

# Активировать виртуальное окружение
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt
```

### Шаг 4: Настройка переменных окружения

```bash
# Создать файл .env
nano .env
```

Вставьте следующее содержимое (замените YOUR_BOT_TOKEN на ваш токен):
```
BOT_TOKEN=YOUR_BOT_TOKEN
WELCOME_IMAGE=images/welcome.jpg
```

Сохраните файл: `Ctrl+O`, `Enter`, затем выйдите: `Ctrl+X`

### Шаг 5: Добавление приветственного изображения

```bash
# Создать директорию для изображений
mkdir -p images

# Вариант 1: Загрузить с локального компьютера через scp
# На вашем локальном компьютере выполните:
# scp /path/to/your/image.jpg root@38.244.194.181:/telebot/images/welcome.jpg

# Вариант 2: Скачать из интернета
# wget -O images/welcome.jpg URL_ИЗОБРАЖЕНИЯ

# Вариант 3: Использовать placeholder изображение
# Если у вас нет изображения, бот будет работать без него
```

### Шаг 6: Сделать скрипт запуска исполняемым

```bash
chmod +x start.sh
```

### Шаг 7: Тестовый запуск

Проверьте, что бот запускается:

```bash
# Активировать виртуальное окружение
source venv/bin/activate

# Запустить бота
python bot.py
```

Если всё работает, вы увидите:
```
INFO - Бот запущен...
```

Остановите бота: `Ctrl+C`

### Шаг 8: Настройка автозапуска через systemd

```bash
# Скопировать service файл
cp telebot.service /etc/systemd/system/

# Перезагрузить конфигурацию systemd
systemctl daemon-reload

# Включить автозапуск
systemctl enable telebot

# Запустить бота
systemctl start telebot

# Проверить статус
systemctl status telebot
```

Вы должны увидеть:
```
● telebot.service - Telegram Bot Service
   Loaded: loaded
   Active: active (running)
```

## Управление ботом

### Основные команды

```bash
# Запустить бота
systemctl start telebot

# Остановить бота
systemctl stop telebot

# Перезапустить бота
systemctl restart telebot

# Проверить статус
systemctl status telebot

# Просмотр логов в реальном времени
journalctl -u telebot -f

# Просмотр последних 100 строк логов
journalctl -u telebot -n 100

# Просмотр логов за сегодня
journalctl -u telebot --since today
```

## Обновление бота

Когда вы внесли изменения в код на GitHub:

```bash
cd /telebot
git pull origin main
systemctl restart telebot
systemctl status telebot
```

## Диагностика проблем

### Проблема 1: Бот не запускается (status=203/EXEC)

**Причина:** Не найден Python или виртуальное окружение

**Решение:**
```bash
cd /telebot

# Проверьте наличие виртуального окружения
ls -la venv/

# Если его нет, создайте
python3 -m venv venv

# Установите зависимости
source venv/bin/activate
pip install -r requirements.txt

# Проверьте права на start.sh
chmod +x start.sh

# Перезапустите сервис
systemctl restart telebot
```

### Проблема 2: Ошибка "BOT_TOKEN не найден"

**Причина:** Не создан файл .env или он пустой

**Решение:**
```bash
cd /telebot

# Проверьте наличие .env
cat .env

# Если файла нет, создайте его
nano .env
```

Добавьте:
```
BOT_TOKEN=ваш_токен_от_botfather
WELCOME_IMAGE=images/welcome.jpg
```

### Проблема 3: Изображение не отправляется

**Причина:** Файл изображения не найден

**Решение:**
```bash
cd /telebot

# Проверьте наличие файла
ls -la images/welcome.jpg

# Если файла нет, загрузите его
# Способ 1: scp с локального компьютера
# scp image.jpg root@38.244.194.181:/telebot/images/welcome.jpg

# Способ 2: wget из интернета
# wget -O images/welcome.jpg URL

# Проверьте права доступа
chmod 644 images/welcome.jpg
```

### Проблема 4: Бот не отвечает на команды

**Проверьте:**

1. Бот запущен:
```bash
systemctl status telebot
```

2. Интернет соединение работает:
```bash
ping -c 4 api.telegram.org
```

3. Токен правильный:
```bash
cat .env | grep BOT_TOKEN
```

4. Проверьте логи:
```bash
journalctl -u telebot -n 50
```

### Проблема 5: Как проверить что виртуальное окружение работает

```bash
cd /telebot
source venv/bin/activate
which python
# Должно вывести: /telebot/venv/bin/python

python --version
# Должна быть версия Python 3.8+
```

## Просмотр логов

### Логи systemd

```bash
# Все логи
journalctl -u telebot

# Последние 50 строк
journalctl -u telebot -n 50

# В реальном времени
journalctl -u telebot -f

# За последний час
journalctl -u telebot --since "1 hour ago"

# За сегодня
journalctl -u telebot --since today

# С определенной даты
journalctl -u telebot --since "2025-11-13"
```

## Безопасность

1. **Никогда не публикуйте .env файл**
```bash
# Проверьте что .env в .gitignore
cat .gitignore | grep .env
```

2. **Регулярно обновляйте зависимости**
```bash
cd /telebot
source venv/bin/activate
pip install --upgrade -r requirements.txt
```

3. **Делайте бэкапы**
```bash
# Бэкап конфигурации
cp .env .env.backup
```

## Полное удаление

Если нужно полностью удалить бота:

```bash
# Остановить и отключить сервис
systemctl stop telebot
systemctl disable telebot
rm /etc/systemd/system/telebot.service
systemctl daemon-reload

# Удалить файлы
rm -rf /telebot

# Или только очистить для переустановки
cd /telebot
rm -rf venv .env
```

## Проверка работы

После установки проверьте бота в Telegram:

1. Найдите вашего бота по имени
2. Нажмите `/start`
3. Должно прийти изображение с кнопкой "Старт"
4. Нажмите на кнопку - должно открыться меню
5. Проверьте все пункты меню

## Контакты для поддержки

При возникновении проблем:
1. Проверьте этот документ
2. Посмотрите логи: `journalctl -u telebot -n 100`
3. Создайте issue на GitHub: https://github.com/Mrktguru/telebot_bot/issues

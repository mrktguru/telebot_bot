# Telegram Bot с меню

Простой Telegram бот с inline кнопками и настраиваемым меню.

## Функционал

- Приветственное сообщение с изображением при команде `/start`
- Inline кнопка "Старт" для перехода в главное меню
- Настраиваемое меню с тремя разделами (легко расширяется):
  - 📰 Новости
  - 🎬 Фильмы
  - ⚽ Спорт
- Каждый раздел содержит ссылки на внешние ресурсы и Telegram каналы
- Возможность легко добавлять новые пункты меню через код

## Требования

- Python 3.8 или выше
- pip (менеджер пакетов Python)

## Установка и настройка

### 1. Создание бота в Telegram

1. Найдите [@BotFather](https://t.me/BotFather) в Telegram
2. Отправьте команду `/newbot`
3. Следуйте инструкциям и получите токен бота
4. Сохраните токен - он понадобится для настройки

### 2. Локальная установка (для тестирования)

```bash
# Клонировать репозиторий
git clone https://github.com/Mrktguru/telebot_bot.git
cd telebot_bot

# Создать виртуальное окружение
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# или
venv\Scripts\activate  # Windows

# Установить зависимости
pip install -r requirements.txt

# Создать файл .env из примера
cp .env.example .env

# Отредактировать .env и добавить токен бота
nano .env
```

### 3. Настройка .env файла

Откройте файл `.env` и заполните необходимые параметры:

```bash
# Токен бота от @BotFather
BOT_TOKEN=ваш_токен_от_botfather

# Путь к приветственному изображению
WELCOME_IMAGE=images/welcome.jpg
```

### 4. Добавление приветственного изображения

Поместите ваше изображение в папку `images/` с именем `welcome.jpg` или измените путь в `.env` файле.

```bash
# Создать директорию для изображений
mkdir -p images

# Скопировать ваше изображение
cp /путь/к/вашему/изображению.jpg images/welcome.jpg
```

### 5. Запуск бота локально

```bash
python bot.py
```

## Деплой на сервер

### Подключение к серверу

```bash
ssh root@38.244.194.181
```

### Установка на сервер

```bash
# Перейти в целевую директорию
cd /telebot

# Клонировать репозиторий (если еще не клонирован)
git clone https://github.com/Mrktguru/telebot_bot.git .

# Или обновить существующий репозиторий
git pull origin main

# Установить Python и pip (если не установлены)
apt update
apt install python3 python3-pip python3-venv -y

# Создать виртуальное окружение
python3 -m venv venv

# Активировать виртуальное окружение
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt

# Создать и настроить .env файл
cp .env.example .env
nano .env
```

### Настройка автозапуска с systemd

Создайте systemd service файл:

```bash
sudo nano /etc/systemd/system/telebot.service
```

Вставьте следующее содержимое:

```ini
[Unit]
Description=Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/telebot
Environment="PATH=/telebot/venv/bin"
ExecStart=/telebot/venv/bin/python /telebot/bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Активируйте и запустите сервис:

```bash
# Перезагрузить конфигурацию systemd
sudo systemctl daemon-reload

# Включить автозапуск
sudo systemctl enable telebot

# Запустить бота
sudo systemctl start telebot

# Проверить статус
sudo systemctl status telebot
```

### Управление ботом на сервере

```bash
# Запуск
sudo systemctl start telebot

# Остановка
sudo systemctl stop telebot

# Перезапуск
sudo systemctl restart telebot

# Просмотр логов
sudo journalctl -u telebot -f

# Просмотр последних 100 строк логов
sudo journalctl -u telebot -n 100
```

### Обновление бота на сервере

```bash
cd /telebot
git pull origin main
sudo systemctl restart telebot
```

## Настройка меню

Все настройки меню находятся в файле `bot.py` в словаре `MENU_ITEMS`. Вы можете легко добавлять новые пункты меню.

### Пример добавления нового пункта:

Откройте `bot.py` и найдите секцию `MENU_ITEMS`:

```python
MENU_ITEMS = {
    'news': {
        'title': '📰 Новости',
        'message': '🗞 Добро пожаловать в раздел новостей!',
        'links': [
            {'text': '🔗 Канал новостей', 'url': 'https://t.me/your_channel'},
            {'text': '🌐 Новостной портал', 'url': 'https://example.com/news'}
        ]
    },
    # Добавьте новый пункт:
    'music': {
        'title': '🎵 Музыка',
        'message': '🎧 Добро пожаловать в раздел музыки!',
        'links': [
            {'text': '🎵 Музыкальный канал', 'url': 'https://t.me/music_channel'},
            {'text': '🌐 Музыкальный портал', 'url': 'https://music.com'}
        ]
    }
}
```

После изменений перезапустите бота:

```bash
sudo systemctl restart telebot
```

## Структура проекта

```
telebot_bot/
├── bot.py              # Основной файл бота
├── .env               # Переменные окружения (не в git)
├── .env.example       # Пример файла с переменными
├── .gitignore        # Игнорируемые файлы
├── requirements.txt   # Зависимости Python
├── README.md         # Документация
└── images/           # Директория для изображений
    └── welcome.jpg   # Приветственное изображение
```

## Решение проблем

### Бот не запускается

1. Проверьте логи: `sudo journalctl -u telebot -f`
2. Убедитесь, что токен бота правильный в `.env`
3. Проверьте, что все зависимости установлены: `pip install -r requirements.txt`

### Бот не отвечает

1. Убедитесь, что бот запущен: `sudo systemctl status telebot`
2. Проверьте интернет-соединение на сервере
3. Убедитесь, что токен бота активен в @BotFather

### Изображение не отображается

1. Убедитесь, что файл изображения существует по пути `images/welcome.jpg`
2. Проверьте права доступа к файлу: `chmod 644 images/welcome.jpg`
3. Убедитесь, что путь в `.env` указан правильно

## Безопасность

- Никогда не коммитьте файл `.env` в git
- Храните токен бота в безопасности
- Регулярно обновляйте зависимости: `pip install --upgrade -r requirements.txt`

## Лицензия

MIT

## Поддержка

При возникновении проблем создайте issue в репозитории GitHub.

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Telegram бот с меню и inline кнопками
"""

import os
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
from dotenv import load_dotenv

# Загрузка переменных окружения
load_dotenv()

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Получение токена бота из переменных окружения
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Путь к приветственному изображению
WELCOME_IMAGE = os.getenv('WELCOME_IMAGE', 'images/welcome.jpg')

# =============================================================================
# КОНФИГУРАЦИЯ МЕНЮ
# Здесь можно легко добавлять новые пункты меню
# =============================================================================

MENU_ITEMS = {
    'news': {
        'title': '📰 Новости',
        'message': '🗞 Добро пожаловать в раздел новостей!\n\nЗдесь вы найдете самые свежие и актуальные новости.',
        'links': [
            {'text': '🔗 Канал новостей', 'url': 'https://t.me/example_news'},
            {'text': '🌐 Новостной портал', 'url': 'https://example.com/news'}
        ]
    },
    'movies': {
        'title': '🎬 Фильмы',
        'message': '🍿 Добро пожаловать в раздел фильмов!\n\nЗдесь вы найдете лучшие фильмы и сериалы.',
        'links': [
            {'text': '🎥 Канал с фильмами', 'url': 'https://t.me/example_movies'},
            {'text': '🌐 Кинопортал', 'url': 'https://example.com/movies'}
        ]
    },
    'sport': {
        'title': '⚽ Спорт',
        'message': '🏆 Добро пожаловать в раздел спорта!\n\nЗдесь вы найдете все о спортивных событиях.',
        'links': [
            {'text': '🏅 Спортивный канал', 'url': 'https://t.me/example_sport'},
            {'text': '🌐 Спортивный портал', 'url': 'https://example.com/sport'}
        ]
    }
}

# Приветственное сообщение
WELCOME_MESSAGE = """
👋 Добро пожаловать!

Я ваш личный помощник. Нажмите кнопку "Старт" чтобы перейти в главное меню.
"""

# Сообщение главного меню
MAIN_MENU_MESSAGE = """
📋 Главное меню

Выберите интересующий вас раздел:
"""


# =============================================================================
# ОБРАБОТЧИКИ КОМАНД
# =============================================================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /start - отправляет приветственное изображение с кнопкой"""
    keyboard = [[InlineKeyboardButton("🚀 Старт", callback_data='main_menu')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Проверяем существование файла изображения
    if os.path.exists(WELCOME_IMAGE):
        try:
            with open(WELCOME_IMAGE, 'rb') as photo:
                await update.message.reply_photo(
                    photo=photo,
                    caption=WELCOME_MESSAGE,
                    reply_markup=reply_markup
                )
        except Exception as e:
            logger.error(f"Ошибка при отправке изображения: {e}")
            # Если ошибка с изображением, отправляем просто текст
            await update.message.reply_text(
                WELCOME_MESSAGE,
                reply_markup=reply_markup
            )
    else:
        # Если файл не найден, отправляем просто текст
        logger.warning(f"Файл изображения не найден: {WELCOME_IMAGE}")
        await update.message.reply_text(
            WELCOME_MESSAGE,
            reply_markup=reply_markup
        )


async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик нажатий на inline кнопки"""
    query = update.callback_query
    await query.answer()

    # Главное меню
    if query.data == 'main_menu':
        keyboard = []

        # Создаем кнопки из конфигурации меню
        for key, item in MENU_ITEMS.items():
            keyboard.append([InlineKeyboardButton(item['title'], callback_data=key)])

        reply_markup = InlineKeyboardMarkup(keyboard)

        # Проверяем, есть ли фото в сообщении
        try:
            if query.message.photo:
                await query.edit_message_caption(
                    caption=MAIN_MENU_MESSAGE,
                    reply_markup=reply_markup
                )
            else:
                await query.edit_message_text(
                    text=MAIN_MENU_MESSAGE,
                    reply_markup=reply_markup
                )
        except Exception as e:
            logger.error(f"Ошибка при редактировании сообщения: {e}")
            # Если не получилось отредактировать, отправляем новое сообщение
            await query.message.reply_text(
                MAIN_MENU_MESSAGE,
                reply_markup=reply_markup
            )

    # Обработка выбора пунктов меню
    elif query.data in MENU_ITEMS:
        item = MENU_ITEMS[query.data]
        keyboard = []

        # Добавляем кнопки со ссылками
        for link in item['links']:
            keyboard.append([InlineKeyboardButton(link['text'], url=link['url'])])

        # Кнопка возврата в главное меню
        keyboard.append([InlineKeyboardButton("⬅️ Назад в меню", callback_data='main_menu')])

        reply_markup = InlineKeyboardMarkup(keyboard)

        # Проверяем, есть ли фото в сообщении
        try:
            if query.message.photo:
                await query.edit_message_caption(
                    caption=item['message'],
                    reply_markup=reply_markup
                )
            else:
                await query.edit_message_text(
                    text=item['message'],
                    reply_markup=reply_markup
                )
        except Exception as e:
            logger.error(f"Ошибка при редактировании сообщения: {e}")
            # Если не получилось отредактировать, отправляем новое сообщение
            await query.message.reply_text(
                item['message'],
                reply_markup=reply_markup
            )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработчик команды /help"""
    help_text = """
ℹ️ Справка по боту

Доступные команды:
/start - Начать работу с ботом
/help - Показать эту справку

Используйте кнопки для навигации по меню.
    """
    await update.message.reply_text(help_text)


def main() -> None:
    """Главная функция запуска бота"""
    if not BOT_TOKEN:
        logger.error("BOT_TOKEN не найден! Проверьте файл .env")
        return

    # Создаем приложение
    application = Application.builder().token(BOT_TOKEN).build()

    # Регистрируем обработчики
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Запускаем бота
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()

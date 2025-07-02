#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Обработчик вебхуков для MAX API
"""

import json
import logging
import os
from typing import Dict, Any

# Импорт модуля погоды
try:
    from bot.weather import get_weather_info
except ImportError:
    # Fallback для локального тестирования
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..'))
    from bot.weather import get_weather_info

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получение токена MAX API из переменных окружения
MAX_API_TOKEN = os.environ.get('MAX_API_TOKEN')

if not MAX_API_TOKEN:
    logger.warning("MAX_API_TOKEN не найден в переменных окружения")


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Обработчик вебхуков от MAX API
    
    Args:
        event: Событие от Netlify
        context: Контекст выполнения
        
    Returns:
        Dict: HTTP ответ
    """
    try:
        # Проверка метода запроса
        http_method = event.get('httpMethod', 'GET')
        
        if http_method != 'POST':
            return {
                'statusCode': 405,
                'headers': {
                    'Content-Type': 'application/json; charset=utf-8',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Method not allowed',
                    'message': 'Только POST запросы разрешены'
                }, ensure_ascii=False)
            }
        
        # Получение тела запроса
        body = event.get('body', '')
        if not body:
            logger.warning("Получен пустой запрос")
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json; charset=utf-8',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Bad request',
                    'message': 'Тело запроса не может быть пустым'
                }, ensure_ascii=False)
            }
        
        # Парсинг JSON
        try:
            webhook_data = json.loads(body)
        except json.JSONDecodeError as e:
            logger.error(f"Ошибка парсинга JSON: {e}")
            return {
                'statusCode': 400,
                'headers': {
                    'Content-Type': 'application/json; charset=utf-8',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({
                    'error': 'Invalid JSON',
                    'message': 'Некорректный формат JSON'
                }, ensure_ascii=False)
            }
        
        logger.info(f"Получен вебхук: {webhook_data}")
        
        # Извлечение данных сообщения
        message_text = webhook_data.get('message', {}).get('text', '').strip()
        user_id = webhook_data.get('message', {}).get('from', {}).get('id')
        chat_id = webhook_data.get('message', {}).get('chat', {}).get('id')
        
        if not message_text:
            logger.warning("Получено сообщение без текста")
            return {
                'statusCode': 200,
                'headers': {
                    'Content-Type': 'application/json; charset=utf-8'
                },
                'body': json.dumps({'status': 'ignored'}, ensure_ascii=False)
            }
        
        # Обработка команд
        response_text = process_message(message_text)
        
        # Формирование ответа для MAX API
        response_data = {
            'method': 'sendMessage',
            'chat_id': chat_id,
            'text': response_text,
            'parse_mode': 'HTML'
        }
        
        logger.info(f"Отправка ответа: {response_text[:100]}...")
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json; charset=utf-8',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps(response_data, ensure_ascii=False)
        }
        
    except Exception as e:
        logger.error(f"Ошибка в обработчике вебхука: {e}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json; charset=utf-8',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': 'Внутренняя ошибка сервера'
            }, ensure_ascii=False)
        }


def process_message(message_text: str) -> str:
    """
    Обрабатывает текст сообщения и возвращает ответ
    
    Args:
        message_text: Текст сообщения от пользователя
        
    Returns:
        str: Ответ бота
    """
    message_text = message_text.strip().lower()
    
    # Команда /start
    if message_text in ['/start', 'start']:
        return (
            "🌤 <b>Добро пожаловать в Погодный бот!</b>\n\n"
            "Я помогу вам узнать актуальную информацию о погоде в любом городе мира.\n\n"
            "<b>Как пользоваться:</b>\n"
            "• Просто напишите название города\n"
            "• Например: <code>Москва</code> или <code>London</code>\n\n"
            "<b>Доступные команды:</b>\n"
            "/start - Показать это сообщение\n"
            "/help - Справка\n\n"
            "Попробуйте прямо сейчас! 🌍"
        )
    
    # Команда /help
    elif message_text in ['/help', 'help', 'помощь']:
        return (
            "🆘 <b>Справка по использованию бота</b>\n\n"
            "<b>Основные функции:</b>\n"
            "• Получение текущей погоды\n"
            "• Поддержка городов по всему миру\n"
            "• Информация на русском языке\n\n"
            "<b>Примеры запросов:</b>\n"
            "• <code>Москва</code>\n"
            "• <code>Санкт-Петербург</code>\n"
            "• <code>New York</code>\n"
            "• <code>Tokyo</code>\n\n"
            "<b>Команды:</b>\n"
            "/start - Главное меню\n"
            "/help - Эта справка\n\n"
            "Если у вас есть вопросы, просто напишите название города! 🌤"
        )
    
    # Обработка запроса погоды
    else:
        # Удаление возможных команд из начала сообщения
        city = message_text.replace('/weather', '').replace('погода', '').strip()
        
        if not city:
            return (
                "❓ <b>Укажите название города</b>\n\n"
                "Пример: <code>Москва</code> или <code>London</code>\n\n"
                "Для справки используйте команду /help"
            )
        
        # Получение информации о погоде
        weather_info = get_weather_info(city)
        
        # Форматирование ответа с HTML разметкой
        if weather_info.startswith('❌'):
            return f"<b>{weather_info}</b>"
        else:
            return f"<b>{weather_info}</b>\n\n💡 Попробуйте другой город или используйте /help для справки"


# Для локального тестирования
if __name__ == '__main__':
    # Тестовый запрос
    test_event = {
        'httpMethod': 'POST',
        'body': json.dumps({
            'message': {
                'text': 'Москва',
                'from': {'id': 123456},
                'chat': {'id': 123456}
            }
        })
    }
    
    result = handler(test_event, None)
    print(json.dumps(result, indent=2, ensure_ascii=False))
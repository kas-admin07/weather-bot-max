#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Главная функция приложения для обработки корневых запросов
"""

import json
from typing import Dict, Any


def handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Обработчик для главной страницы бота
    
    Args:
        event: Событие от Netlify
        context: Контекст выполнения
        
    Returns:
        Dict: HTTP ответ с информацией о боте
    """
    return {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'application/json; charset=utf-8',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps({
            'status': 'running',
            'service': 'MAX Weather Bot',
            'description': 'Погодный бот для платформы MAX',
            'version': '1.0.0',
            'endpoints': {
                'webhook': '/webhook/max',
                'health': '/health'
            },
            'features': [
                'Получение текущей погоды',
                'Поддержка городов по всему миру',
                'Русский интерфейс',
                'Интеграция с MAX API'
            ]
        }, ensure_ascii=False)
    }